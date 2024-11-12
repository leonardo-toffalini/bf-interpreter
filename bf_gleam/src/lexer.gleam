import simplifile
import token
import gleam/list
import gleam/string

pub fn lex(filepath: String) -> List(token.Token) {
  case simplifile.read(filepath) {
    Ok(source) -> do_lex(source, 0, [])
    Error(_) -> panic
  }
}

fn do_lex(source: String, index: Int, acc: List(token.Token)) -> List(token.Token) {
  case string.pop_grapheme(source) {
    Error(Nil) -> acc |> list.reverse  // got to the end of the source
    Ok(#(first, rest)) -> case first, rest {
    ">", rest -> do_lex(rest, index+1, [token.Token(token.Increment, index, -1, 1), ..acc])
    "<", rest -> do_lex(rest, index+1, [token.Token(token.Decrement, index, -1, 1), ..acc])
    "+", rest -> do_lex(rest, index+1, [token.Token(token.Plus, index, -1, 1), ..acc])
    "-", rest -> do_lex(rest, index+1, [token.Token(token.Minus, index, -1, 1), ..acc])
    ".", rest -> do_lex(rest, index+1, [token.Token(token.Dot, index, -1, 1), ..acc])
    ",", rest -> do_lex(rest, index+1, [token.Token(token.Comma, index, -1, 1), ..acc])
    "[", rest -> do_lex(rest, index+1, [token.Token(token.Lbracket, index, -1, 1), ..acc])
    "]", rest -> do_lex(rest, index+1, [token.Token(token.Rbracket, index, -1, 1), ..acc])
    _, rest -> do_lex(rest, index, acc)  // all other characters are considered comment
    }
  }
}

