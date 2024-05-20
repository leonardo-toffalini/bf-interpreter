from icecream import ic
from enum import Enum, auto


class TokenType(Enum):
    increment = auto()
    decrement = auto()
    plus = auto()
    minus = auto()
    dot = auto()
    comma = auto()
    lbracket = auto()
    rbracket = auto()


class Token:
    def __init__(self, ttype, pos, address=None):
        self.ttype = ttype
        self.pos = pos
        self.address = address

    def __repr__(self):
        return (
            f"Token(TokneType: {self.ttype}, pos: {self.pos}, address: {self.address})"
        )


def read_tokens(file_path):
    with open(file_path, "r") as f:
        raw = f.read()

    tokens = []
    index = 0
    for char in raw:
        if char in "><+-.,[]":
            if char == ">":
                tokens.append(Token(TokenType.increment, index))
                index += 1
            elif char == "<":
                tokens.append(Token(TokenType.decrement, index))
                index += 1
            elif char == "+":
                tokens.append(Token(TokenType.plus, index))
                index += 1
            elif char == "-":
                tokens.append(Token(TokenType.minus, index))
                index += 1
            elif char == ".":
                tokens.append(Token(TokenType.dot, index))
                index += 1
            elif char == ",":
                tokens.append(Token(TokenType.comma, index))
                index += 1
            elif char == "[":
                tokens.append(Token(TokenType.lbracket, index))
                index += 1
            elif char == "]":
                tokens.append(Token(TokenType.rbracket, index))
                index += 1
            else:
                assert False, "Unexpected token in read_tokens()"

    return tokens


def cross_reference_porgram(tokens):
    index = 0
    pos_of_lbracket = -1
    while index < len(tokens):
        token = tokens[index]
        if token.ttype == TokenType.lbracket:
            pos_of_lbracket = index
        if token.ttype == TokenType.rbracket:
            token.address = pos_of_lbracket
            tokens[pos_of_lbracket].address = index
        index += 1


def simulate_program(tokens):
    byte_array_size = 30_000
    byte_array = bytearray(byte_array_size)
    reader_pos = 0

    for token in tokens:
        if token.ttype == TokenType.increment:
            reader_pos += 1
        if token.ttype == TokenType.decrement:
            reader_pos -= 1
        if token.ttype == TokenType.plus:
            byte_array[reader_pos] += 1
        if token.ttype == TokenType.minus:
            byte_array[reader_pos] -= 1
        if token.ttype == TokenType.dot:
            print(byte_array[reader_pos])
        if token.ttype == TokenType.comma:
            raise NotImplementedError
        if token.ttype == TokenType.lbracket:
            raise NotImplementedError
        if token.ttype == TokenType.rbracket:
            raise NotImplementedError


def main():
    file_path = "example.bf"
    tokens = read_tokens(file_path)
    ic(tokens)
    cross_reference_porgram(tokens)
    ic(tokens)
    # simulate_program(tokens)


if __name__ == "__main__":
    main()
