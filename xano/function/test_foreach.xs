function test_foreach {
  input {
  }

  stack {
    db.query user {
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
  }

  response = null
  guid = "TdzkX--M4Znb5d7GWz2uCm-EGhM"
}