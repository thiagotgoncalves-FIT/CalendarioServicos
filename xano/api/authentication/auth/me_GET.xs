query "auth/me" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "created_at", "name", "email", "phone", "role"]
    } as $current_user
  
    precondition ($current_user != null) {
      error_type = "notfound"
      error = "Usuário autenticado não encontrado."
    }
  }

  response = $current_user
  guid = "mEO2BL83xyDDuPXrlzzEHRcmLdQ"
}