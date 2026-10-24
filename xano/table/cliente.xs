// CLIENTE
table CLIENTE {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    int user_id? {
      table = "user"
    }
  
    text celular? filters=trim
    text cpf? filters=trim
    int status_cliente_id?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree|unique", field: [{name: "cpf", op: "asc"}]}
  ]

  guid = "M9DOxtFiGZAHJwiV-7zOhh00SWQ"
  items = []
}