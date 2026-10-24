query "auth/signup" verb=POST {
  api_group = "Authentication"

  input {
    text name filters=trim
    email email filters=trim|lower
    password password filters=min:8|minAlpha:1|minDigit:1
    text phone? filters=trim
    enum role? {
      values = ["prestador", "cliente"]
    }
  }

  stack {
    // 1. Verificar se o e-mail ja existe
    db.get user {
      field_name = "email"
      field_value = $input.email
    } as $existing_user
  
    precondition ($existing_user == null) {
      error_type = "badrequest"
      error = "Este endereço de e-mail já está em uso."
    }
  
    // 2. Criar novo usuario na tabela
    db.add user {
      enforce_hidden_fields = false
      data = {
        created_at: "now"
        name      : $input.name
        email     : $input.email
        password  : $input.password
        phone     : $input.phone
        role      : $input.role
      }
    } as $new_user
  
    // 3. Gerar o token de autenticacao
    security.create_auth_token {
      table = "user"
      extras = {role: $new_user.role}
      expiration = 86400
      id = $new_user.id
    } as $authToken
  }

  response = {authToken: $authToken, user: $new_user}
  guid = "9KmiWb4bvA_MndzEatGupA_3l2A"
}