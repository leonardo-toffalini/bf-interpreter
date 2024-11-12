import gleeunit
import gleeunit/should
import token.{Token, token_to_string}

pub fn main() {
  gleeunit.main()
}

// gleeunit test functions end in `_test`
pub fn hello_world_test() {
  1
  |> should.equal(1)
}

pub fn token_to_string_test() {
  let t = Token(token.Increment, 1, 1, 1)
  token_to_string(t)
  |> should.equal("Token(type: increment, position: 1, address: 1, value: 1)")
}
