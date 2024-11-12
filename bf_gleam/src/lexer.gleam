import gleam/list
import gleam/string
import simplifile
import token

pub fn lex(filepath: String) -> List(token.Token) {
  case simplifile.read(filepath) {
    Ok(source) -> do_lex(source, 0, [])
    Error(_) -> panic
  }
}

fn do_lex(
  source: String,
  index: Int,
  acc: List(token.Token),
) -> List(token.Token) {
  let template = token.Token(token.Plus, index, -1, 1)
  case string.pop_grapheme(source) {
    Error(Nil) -> acc |> list.reverse
    // got to the end of the source
    Ok(#(first, rest)) ->
      case first, rest {
        ">", rest ->
          do_lex(rest, index + 1, [
            token.Token(..template, token_type: token.Increment),
            ..acc
          ])
        "<", rest ->
          do_lex(rest, index + 1, [
            token.Token(..template, token_type: token.Decrement),
            ..acc
          ])
        "+", rest ->
          do_lex(rest, index + 1, [
            token.Token(..template, token_type: token.Plus),
            ..acc
          ])
        "-", rest ->
          do_lex(rest, index + 1, [
            token.Token(..template, token_type: token.Minus),
            ..acc
          ])
        ".", rest ->
          do_lex(rest, index + 1, [
            token.Token(..template, token_type: token.Dot),
            ..acc
          ])
        ",", rest ->
          do_lex(rest, index + 1, [
            token.Token(..template, token_type: token.Comma),
            ..acc
          ])
        "[", rest ->
          do_lex(rest, index + 1, [
            token.Token(..template, token_type: token.Lbracket),
            ..acc
          ])
        "]", rest ->
          do_lex(rest, index + 1, [
            token.Token(..template, token_type: token.Rbracket),
            ..acc
          ])
        _, rest -> do_lex(rest, index, acc)
        // all other characters are considered comment
      }
  }
}

pub fn cross_reference_tokens(tokens: List(token.Token)) -> List(token.Token) {
  let len = list.length(tokens) - 1
  tokens
  |> forward(0, [], [])
  |> list.reverse
  |> backward(len, [], [])
  |> list.reverse
}

// [[]>>+++<-[++<-]]
// 0 1 2 3 4 5 6 7 
// [ [ [ ] [ ] ] ]
// x x x 2 x 4 1 0  forward pass
// 7 6 3 x 5 x x x  backward pass
// 7 6 3 2 5 4 1 0  the two together

fn forward(
  tokens: List(token.Token),
  index: Int,
  stack: List(Int),
  acc: List(token.Token),
) -> List(token.Token) {
  case tokens {
    [] -> acc |> list.reverse
    [first, ..rest] ->
      case first.token_type {
        // push index to stack
        token.Lbracket ->
          forward(rest, index + 1, [index, ..stack], [first, ..acc])
        token.Rbracket ->
          case stack {
            [] -> panic
            // pop index from stack and write it as address
            [pop, ..tail] ->
              forward(rest, index + 1, tail, [
                token.Token(..first, address: pop),
                ..acc
              ])
          }
        _ -> forward(rest, index + 1, stack, [first, ..acc])
      }
  }
}

fn backward(
  tokens: List(token.Token),
  index: Int,
  stack: List(Int),
  acc: List(token.Token),
) -> List(token.Token) {
  case tokens {
    [] -> acc |> list.reverse
    [last, ..rest] ->
      case last.token_type {
        token.Rbracket ->
          backward(rest, index - 1, [index, ..stack], [last, ..acc])
        token.Lbracket ->
          case stack {
            [] -> panic
            [pop, ..tail] ->
              backward(rest, index - 1, tail, [
                token.Token(..last, address: pop),
                ..acc
              ])
          }
        _ -> backward(rest, index - 1, stack, [last, ..acc])
      }
  }
}

