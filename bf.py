from enum import Enum, auto
import sys


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
        else:
            pass  # comments

    return tokens


def cross_reference_porgram(tokens):
    index = 0
    bracket_stack = []
    while index < len(tokens):
        token = tokens[index]
        if token.ttype == TokenType.lbracket:
            bracket_stack.append(index)
        if token.ttype == TokenType.rbracket:
            prev_lbracket_pos = bracket_stack.pop()
            token.address = prev_lbracket_pos
            tokens[prev_lbracket_pos].address = index
        index += 1


def pretty_print_byte_array(array, reader_pos, size):
    pos = 1
    for i in range(size):
        if i == reader_pos:
            print(f"\033[1;31m[{array[i]}]\033[0m", end="")
        else:
            print(f"[{array[i]}]", end="")

        if i < reader_pos:
            pos += 2 + len(str(array[i]))

    print("\n" + (" " * pos) + "\033[0;32m^\033[0m")


def simulate_program(tokens, debug=0):
    byte_array_size = 30_000
    byte_array = bytearray(byte_array_size)
    reader_pos = 0

    index = 0
    while index < len(tokens):
        if debug > 0:
            pretty_print_byte_array(byte_array, reader_pos, debug)

        token = tokens[index]
        if token.ttype == TokenType.increment:
            reader_pos += 1
            index += 1
        if token.ttype == TokenType.decrement:
            reader_pos -= 1
            index += 1
        if token.ttype == TokenType.plus:
            byte_array[reader_pos] = (byte_array[reader_pos] + 1) % 256
            index += 1
        if token.ttype == TokenType.minus:
            byte_array[reader_pos] = (byte_array[reader_pos] - 1) % 256
            index += 1
        if token.ttype == TokenType.dot:
            print(chr(byte_array[reader_pos]), end="")
            index += 1
        if token.ttype == TokenType.comma:
            x = ord(sys.stdin.read(1)) % 256
            byte_array[reader_pos] = x
            index += 1
        if token.ttype == TokenType.lbracket:
            if byte_array[reader_pos] == 0:
                index = token.address + 1
            else:
                index += 1

        if token.ttype == TokenType.rbracket:
            index = token.address


def print_usage():
    print("Usage:")
    print("\tProvide the path of the programan to simulate.")
    print("\tFor example:")
    print("\t\t```$ python3 bf.py example/hello_world.bf```\n")
    print("\tAdditionally, you can enable debug mode with the `-debug=n` flag,")
    print("\twhere n is the number of cells from the byte array to print")
    print("\tFor example:")
    print("\t\t```$ python3 bf.py example/hello_world.bf -debug=10```\n")


def main():
    if len(sys.argv) < 2:
        print_usage()
        exit(1)

    file_path = sys.argv[1]
    debug = 0

    if len(sys.argv) == 3:
        debug = int(sys.argv[2].split("=")[-1])
    elif len(sys.argv) > 3:
        print_usage()

    tokens = read_tokens(file_path)
    cross_reference_porgram(tokens)
    simulate_program(tokens, debug)


if __name__ == "__main__":
    main()
