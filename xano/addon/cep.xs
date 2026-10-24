addon CEP {
  input {
    int CEP_id? {
      table = ""
    }
  }

  stack {
    db.query "" {
      where = $db.CEP.id == $input.CEP_id
      return = {type: "single"}
    }
  }

  guid = "ELncJz6RIOOqRcRe1NSl1aexmpo"
}