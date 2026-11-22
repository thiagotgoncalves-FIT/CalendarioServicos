// Stores user information and allows the user to authenticate  against
table user {
  auth = true

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text name filters=trim
    email? email filters=trim|lower
    password? password filters=min:8|minAlpha:1|minDigit:1 {
      visibility = "internal"
    }
  
    // Reference to the company the user belongs to.
    int account_id? {
      table = "account"
    }
  
    // Perfil de acesso do usuário na plataforma AgendAí.
    enum role? {
      values = ["prestador", "cliente"]
      visibility = "private"
    }
  
    // Número de telefone/celular do usuário.
    text phone? filters=trim
  
    object password_reset? {
      schema {
        password token? {
          visibility = "internal"
        }
      
        timestamp? expiration? {
          visibility = "internal"
        }
      
        bool used? {
          visibility = "internal"
        }
      }
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree|unique", field: [{name: "email", op: "asc"}]}
  ]

  tags = ["xano:quick-start"]
  guid = "zc9CNCMCh14FUEMIRcJOy85WCkw"
  items = [
    {
      id            : 15
      created_at    : 1791939376230
      name          : "Hector Barros"
      email         : "hector.barros@aluno.impacta.edu.br"
      password      : "993c7fd8fd8f9656.0c0a2e06ffbc51664a947370f6805a943c75db785999943dbe01bee37b004fe4"
      account_id    : 0
      role          : "prestador"
      password_reset: {used: false, token: "", expiration: null}
      phone         : "11989898768"
    }
  ]
}