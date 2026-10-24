query "auth/login" verb=POST {
  api_group = "Authentication"

  input {
    email email filters=trim|lower
    text password
  }

  stack {
    // 1. Buscar usuario pelo e-mail com output explicito contendo password
    db.query user {
      where = $db.user.email == $input.email
      return = {type: "single"}
      output = ["id", "created_at", "name", "email", "phone", "role", "password"]
    } as $user
  
    // 2. Validar existencia do usuario
    precondition ($user != null) {
      error_type = "accessdenied"
      error = "Credenciais inválidas ou e-mail não cadastrado."
    }
  
    // 3. Validar a senha com o hash do Xano
    security.check_password {
      text_password = $input.password
      hash_password = $user.password
    } as $pass_result
  
    precondition ($pass_result) {
      error_type = "accessdenied"
      error = "Senha incorreta. Verifique suas credenciais."
    }
  
    // 4. Gerar o token de autenticacao
    security.create_auth_token {
      table = "user"
      extras = {role: $user.role}
      expiration = 86400
      id = $user.id
    } as $authToken
  }

  response = {
    authToken: $authToken
    user     : ```
      {
        id        : $user.id
        name      : $user.name
        email     : $user.email
        phone     : $user.phone
        role      : $user.role
        created_at: $user.created_at
      }
      ```
  }

  guid = "090WQME4APdnAEOBZwUW3vi9rpA"
}