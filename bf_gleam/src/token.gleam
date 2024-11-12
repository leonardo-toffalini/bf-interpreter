import gleam/io
import gleam/int

pub type TokenType {
  Increment
  Decrement
  Plus
  Minus
  Dot
  Comma
  Lbracket
  Rbracket
}

pub type Token {
  Token(
  token_type: TokenType,
  position: Int,
  address: Int,
  value: Int
)
}

pub fn token_to_string(t: Token) -> String {
  "Token(type: " <>
  case t.token_type {
    Increment -> "increment"
    Decrement -> "decrement"
    Plus -> "plus"
    Minus -> "minus"
    Dot -> "dot"
    Comma -> "comma"
    Lbracket -> "lbracket"
    Rbracket -> "rbracket"
  }
  <> ", position: " <> int.to_string(t.position)
  <> ", address: " <> int.to_string(t.address)
  <> ", value: " <> int.to_string(t.value)
  <> ")"
}

pub fn print_token(t: Token) -> Nil {
  io.println(token_to_string(t))
}
