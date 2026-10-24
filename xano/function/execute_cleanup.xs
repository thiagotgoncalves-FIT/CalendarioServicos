function execute_cleanup {
  input {
  }

  stack {
    // 1. Apagar registros dependentes da tabela CLIENTE
    db.query CLIENTE {
      return = {type: "list"}
    } as $clientes
  
    foreach ($clientes) {
      each as $c {
        db.del CLIENTE {
          field_name = "id"
          field_value = $c.id
        }
      }
    }
  
    // 2. Apagar registros dependentes da tabela event_log
    db.query event_log {
      return = {type: "list"}
    } as $logs
  
    foreach ($logs) {
      each as $l {
        db.del event_log {
          field_name = "id"
          field_value = $l.id
        }
      }
    }
  
    // 3. Apagar todos os usuários exceto o Hector (id 15)
    db.query user {
      where = $db.user.id != 15
      return = {type: "list"}
    } as $users
  
    foreach ($users) {
      each as $u {
        db.del user {
          field_name = "id"
          field_value = $u.id
        }
      }
    }
  
    // 4. Padronizar o nome do Hector para 'Hector Barros'
    db.patch user {
      field_name = "id"
      field_value = 15
      data = {name: "Hector Barros"}
    } as $hector
  }

  response = {
    clientes_deleted: $clientes|count
    logs_deleted    : $logs|count
    users_deleted   : $users|count
    hector          : $hector
  }

  guid = "c7n_rkdo3qf-JlUdhfWy2t8awNM"
}