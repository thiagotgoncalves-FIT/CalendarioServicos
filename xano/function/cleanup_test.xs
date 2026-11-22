function cleanup_test {
  input {
  }

  stack {
    db.query user {
      return = {type: "list"}
    } as $users
  }

  response = $users
  guid = "agHVFAkYvNn0ni_41wWWGdOfeIY"
}