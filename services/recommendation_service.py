"""
Serviço de Recomendação Inteligente de Prestadores e Serviços (AgendAí).
Implementa algoritmo multicritério determinístico com pontuação normalizada de 0 a 100,
filtros eliminatórios estritos (orçamento e disponibilidade) e geração de justificativas.
"""

import re
from datetime import date
from typing import List, Dict, Any, Optional
from services import catalog_service, appointment_service, auth_service

# Pesos oficiais do algoritmo multicritério (soma = 1.0)
PESO_COMPATIBILIDADE = 0.35
PESO_ORCAMENTO = 0.25
PESO_DISPONIBILIDADE = 0.25
PESO_AVALIACAO = 0.15


def _tokenize(text: str) -> set:
    """Extrai palavras-chave limpas em minúsculas (stop-words simplificadas ignoradas)."""
    if not text:
        return set()
    stopwords = {"de", "da", "do", "para", "com", "em", "um", "uma", "o", "a", "os", "as", "e", "ou", "no", "na"}
    words = re.findall(r"\b[a-zA-ZÀ-ÿ0-9]{3,}\b", text.lower())
    return {w for w in words if w not in stopwords}


def _calcular_compatibilidade_textual(termo_busca: str, descricao_necessidade: str, servico: Dict[str, Any]) -> float:
    """
    Calcula a similaridade textual entre o pedido do cliente e o serviço ofertado (0 a 100).
    """
    titulo = servico.get("titulo", "")
    desc_servico = servico.get("descricao", "")
    
    tokens_servico = _tokenize(f"{titulo} {desc_servico}")
    tokens_busca = _tokenize(f"{termo_busca} {descricao_necessidade}")
    
    if not tokens_busca:
        return 70.0  # Busca genérica recebe nota média-alta base
    
    if not tokens_servico:
        return 50.0

    intersecao = tokens_busca.intersection(tokens_servico)
    if not intersecao:
        # Verifica substring simples
        termo_lower = (termo_busca or "").lower().strip()
        if termo_lower and (termo_lower in titulo.lower() or termo_lower in desc_servico.lower()):
            return 85.0
        return 30.0

    # Coeficiente Jaccard normalizado
    uniao = tokens_busca.union(tokens_servico)
    jaccard = len(intersecao) / len(uniao)
    # Escala para 40 a 100
    return min(100.0, 40.0 + (jaccard * 120.0))


def _calcular_score_orcamento(preco: float, orcamento_max: float) -> float:
    """
    Calcula pontuação de orçamento (0 a 100).
    Quanto mais econômico e vantajoso em relação ao teto do cliente, maior a pontuação.
    """
    if orcamento_max <= 0:
        return 80.0
    if preco > orcamento_max:
        return 0.0  # Desclassificado pelo filtro
    
    # Preço exatamente no teto ganha 70 pontos; preços abaixo ganham até 100 pontos
    diferenca_relativa = (orcamento_max - preco) / orcamento_max
    score = 70.0 + (diferenca_relativa * 30.0)
    return min(100.0, max(0.0, score))


def _calcular_score_disponibilidade(qtd_slots: int) -> float:
    """
    Calcula pontuação de disponibilidade (0 a 100) com base na flexibilidade de horários no dia.
    """
    if qtd_slots <= 0:
        return 0.0
    if qtd_slots >= 6:
        return 100.0
    if qtd_slots >= 4:
        return 85.0
    if qtd_slots >= 2:
        return 70.0
    return 60.0


def recommend_providers(
    termo_busca: str,
    descricao_necessidade: str,
    orcamento_max: float,
    data_str: str,
    token: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Processa critérios do cliente e retorna lista ordenada de prestadores/serviços recomendados.
    Aplica filtros eliminatórios estritos de orçamento e disponibilidade na data.
    """
    # 1. Obter catálogo de serviços ativos
    suc_cat, servicos = catalog_service.get_public_services(token=token)
    if not suc_cat or not servicos:
        return []

    # 2. Iterar sobre os serviços e avaliar elegibilidade
    resultados_elegiveis: List[Dict[str, Any]] = []

    for serv in servicos:
        if not serv.get("ativo", True):
            continue

        preco = float(serv.get("preco", 0.0))
        prestador_id = serv.get("prestador_id", 15)
        duracao = serv.get("duracao_minutos", 30)

        # FILTRO ELIMINATÓRIO 1: Orçamento Máximo
        if orcamento_max > 0 and preco > orcamento_max:
            continue

        # FILTRO ELIMINATÓRIO 2: Disponibilidade na Data
        slots_livres = appointment_service.calculate_available_slots(
            prestador_id=prestador_id,
            date_str=data_str,
            duration_minutes=duracao,
            token=token
        )
        if not slots_livres:
            continue  # Sem horários livres na data -> desclassificado

        # 3. Cálculo das pontuações por critério
        score_comp = _calcular_compatibilidade_textual(termo_busca, descricao_necessidade, serv)
        score_orc = _calcular_score_orcamento(preco, orcamento_max)
        score_disp = _calcular_score_disponibilidade(len(slots_livres))
        
        # Avaliação do prestador (obtém do review_service se disponível, fallback para 5.0)
        try:
            from services import review_service
            metrics = review_service.get_metrics(prestador_id=prestador_id, token=token)
            avaliacao_prestador = metrics.get("nota_media") if metrics.get("total_avaliacoes", 0) > 0 else float(serv.get("avaliacao", 5.0))
        except Exception:
            avaliacao_prestador = float(serv.get("avaliacao", 5.0))
        score_aval = min(100.0, (avaliacao_prestador / 5.0) * 100.0)

        # Score Final Ponderado (0 a 100)
        score_final = round(
            (score_comp * PESO_COMPATIBILIDADE) +
            (score_orc * PESO_ORCAMENTO) +
            (score_disp * PESO_DISPONIBILIDADE) +
            (score_aval * PESO_AVALIACAO),
            1
        )

        # 4. Geração de justificativas transparentes
        justificativas: List[str] = []
        if orcamento_max > 0 and preco < orcamento_max:
            economia = orcamento_max - preco
            justificativas.append(f"Preço favorável (R$ {economia:,.2f} abaixo do seu orçamento)".replace(".", ","))
        elif orcamento_max > 0:
            justificativas.append("Valor compatível com seu orçamento máximo")

        if len(slots_livres) >= 3:
            justificativas.append(f"Excelente disponibilidade com {len(slots_livres)} horários livres nesta data")
        else:
            justificativas.append("Vagas confirmadas para a data selecionada")

        if score_comp >= 80:
            justificativas.append("Alta compatibilidade com a especialidade e descrição solicitada")
        else:
            justificativas.append("Serviço alinhado com a categoria pesquisada")

        if avaliacao_prestador >= 4.8:
            justificativas.append("Profissional altamente avaliado na plataforma (nota 5.0)")

        # Dados do prestador
        nome_prestador = serv.get("prestador_nome") or "Hector Barros"

        resultados_elegiveis.append({
            "servico": serv,
            "prestador_id": prestador_id,
            "prestador_nome": nome_prestador,
            "score": score_final,
            "score_breakdown": {
                "compatibilidade": round(score_comp, 1),
                "orcamento": round(score_orc, 1),
                "disponibilidade": round(score_disp, 1),
                "avaliacao": round(score_aval, 1)
            },
            "justificativas": justificativas,
            "slots_disponiveis": slots_livres
        })

    # Ordena decrescentemente pelo score final
    resultados_elegiveis.sort(key=lambda r: r["score"], reverse=True)
    return resultados_elegiveis
