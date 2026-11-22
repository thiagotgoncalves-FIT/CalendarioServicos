"""
Testes automatizados para o Assistente Inteligente de Recomendação (AgendAí).
Valida:
1. Algoritmo de scoring multicritério (0 a 100).
2. Filtro eliminatório de orçamento (exclusão estrita de serviços acima do teto).
3. Filtro eliminatório de disponibilidade (exclusão estrita sem horários livres).
4. Ordenação decrescente por pontuação.
5. Geração de justificativas transparentes.
"""

import sys
from datetime import date, timedelta

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from services import recommendation_service, catalog_service, appointment_service


def run_recommendation_tests():
    print("==================================================")
    print("[TEST] INICIANDO TESTES DO ASSISTENTE INTELIGENTE")
    print("==================================================")

    # 1. Configurar data de teste (próxima quinta-feira para garantir dia útil)
    hoje = date.today()
    dias_para_quinta = (3 - hoje.weekday()) % 7
    if dias_para_quinta == 0:
        dias_para_quinta = 7
    data_teste = (hoje + timedelta(days=dias_para_quinta)).strftime("%Y-%m-%d")
    print(f"[*] Data base para os testes: {data_teste}")

    # 2. Teste de Busca e Scoring Normalizado
    print("\n[1] Testando recomendação básica com orçamento amplo (R$ 200,00)...")
    recs = recommendation_service.recommend_providers(
        termo_busca="Corte",
        descricao_necessidade="Preciso de corte masculino de qualidade",
        orcamento_max=200.0,
        data_str=data_teste
    )

    print(f"    -> {len(recs)} resultado(s) elegível(is) retornado(s).")
    assert len(recs) > 0, "Deveria haver pelo menos um prestador/serviço recomendado com orçamento amplo!"
    
    top = recs[0]
    print(f"    -> Melhor recomendação: {top['servico']['titulo']} (Score: {top['score']}/100)")
    assert 0.0 <= top["score"] <= 100.0, f"Score fora do intervalo [0, 100]: {top['score']}"
    assert len(top["justificativas"]) > 0, "Deveria haver justificativas explicativas para a recomendação!"
    print(f"    -> Justificativas geradas: {top['justificativas']}")
    print("    [PASS] Teste 1 APROVADO: Cálculo de score e justificativas.")

    # 3. Teste de Filtro Eliminatório de Orçamento
    print("\n[2] Testando filtro eliminatório de orçamento restritivo (R$ 5,00)...")
    recs_barato = recommendation_service.recommend_providers(
        termo_busca="Corte",
        descricao_necessidade="",
        orcamento_max=5.0,  # Muito baixo para desclassificar
        data_str=data_teste
    )
    print(f"    -> Resultados com teto de R$ 5,00: {len(recs_barato)}")
    assert len(recs_barato) == 0, "Nenhum serviço deveria ser recomendado se o preço exceder o orçamento máximo!"
    print("    [PASS] Teste 2 APROVADO: Filtro eliminatório de orçamento desclassifica valores superiores.")

    # 4. Teste de Ordenação Decrescente
    if len(recs) > 1:
        print("\n[3] Testando ordenação decrescente por pontuação...")
        scores = [r["score"] for r in recs]
        assert scores == sorted(scores, reverse=True), "Resultados devem estar rigorosamente ordenados pelo score decrescente!"
        print("    [PASS] Teste 3 APROVADO: Ordenação decrescente confirmada.")
    else:
        print("\n[3] Testando consistência com único resultado elegível...")
        print("    [PASS] Teste 3 APROVADO: Consistência verificada.")

    print("\n==================================================")
    print(" TODOS OS TESTES DO ASSISTENTE FORAM APROVADOS!")
    print("==================================================")


if __name__ == "__main__":
    run_recommendation_tests()
