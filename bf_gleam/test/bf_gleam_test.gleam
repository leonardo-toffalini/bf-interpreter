import gleeunit
import gleeunit/should
import lexer
import simplifile
import token.{Token, token_to_string}

pub fn main() {
  gleeunit.main()
}

pub fn token_to_string_1_test() {
  let t = Token(token.Increment, 1, 1, 1)
  token_to_string(t)
  |> should.equal("Token(type: increment, position: 1, address: 1, value: 1)")

  let t = Token(token.Decrement, 1, 1, 1)
  token_to_string(t)
  |> should.equal("Token(type: decrement, position: 1, address: 1, value: 1)")

  let t = Token(token.Plus, 1, 1, 1)
  token_to_string(t)
  |> should.equal("Token(type: plus, position: 1, address: 1, value: 1)")

  let t = Token(token.Minus, 1, 1, 1)
  token_to_string(t)
  |> should.equal("Token(type: minus, position: 1, address: 1, value: 1)")

  let t = Token(token.Dot, 1, 1, 1)
  token_to_string(t)
  |> should.equal("Token(type: dot, position: 1, address: 1, value: 1)")

  let t = Token(token.Comma, 1, 1, 1)
  token_to_string(t)
  |> should.equal("Token(type: comma, position: 1, address: 1, value: 1)")

  let t = Token(token.Lbracket, 1, 1, 1)
  token_to_string(t)
  |> should.equal("Token(type: lbracket, position: 1, address: 1, value: 1)")

  let t = Token(token.Rbracket, 1, 1, 1)
  token_to_string(t)
  |> should.equal("Token(type: rbracket, position: 1, address: 1, value: 1)")
}

pub fn read_file_test() {
  let filepath = "examples/hello_world.bf"
  simplifile.read(filepath)
  |> should.equal(Ok(
    "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.\n",
  ))
}

pub fn lex_file_test() {
  let filepath = "examples/two_five.bf"
  lexer.lex(filepath)
  |> should.equal([
    Token(token.Plus, 0, -1, 1),
    Token(token.Plus, 1, -1, 1),
    Token(token.Increment, 2, -1, 1),
    Token(token.Plus, 3, -1, 1),
    Token(token.Plus, 4, -1, 1),
    Token(token.Plus, 5, -1, 1),
    Token(token.Plus, 6, -1, 1),
    Token(token.Plus, 7, -1, 1),
  ])
}
