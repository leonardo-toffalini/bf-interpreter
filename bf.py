from enum import Enum, auto
import sys
import subprocess

# from icecream import ic


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
    def __init__(self, ttype, pos, address=None, value=None):
        self.ttype = ttype
        self.pos = pos
        self.address = address
        self.value = value  # indicates how many of them are in a row for tokens ><+-

    def __repr__(self):
        return f"Token(TokneType: {self.ttype}, pos: {self.pos}, address: {self.address}, value: {self.value})"


def read_tokens(file_path):
    with open(file_path, "r") as f:
        raw = f.read()

    tokens = []
    index = 0
    for char in raw:
        if char in "><+-.,[]":
            if char == ">":
                tokens.append(Token(TokenType.increment, index, value=1))
                index += 1
            elif char == "<":
                tokens.append(Token(TokenType.decrement, index, value=1))
                index += 1
            elif char == "+":
                tokens.append(Token(TokenType.plus, index, value=1))
                index += 1
            elif char == "-":
                tokens.append(Token(TokenType.minus, index, value=1))
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


def collapse_runs(tokens):
    i = 0
    while i < len(tokens):
        current_token = tokens[i]

        if current_token.ttype not in [
            TokenType.increment,
            TokenType.decrement,
            TokenType.plus,
            TokenType.minus,
        ]:
            i += 1
            continue

        j = i + 1
        while j < len(tokens) and tokens[j].ttype == current_token.ttype:
            current_token.value += 1
            tokens.pop(j)
        i += 1


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
            reader_pos += token.value
            index += 1
        if token.ttype == TokenType.decrement:
            reader_pos -= token.value
            index += 1
        if token.ttype == TokenType.plus:
            byte_array[reader_pos] = (byte_array[reader_pos] + token.value) % 256
            index += 1
        if token.ttype == TokenType.minus:
            byte_array[reader_pos] = (byte_array[reader_pos] - token.value) % 256
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


def transpile_program(tokens):
    with open("out.c", "w") as f:

        f.write("#include <stdio.h>\n\n")
        f.write("int main(void) {\n")
        f.write("\tint byte_array[100000];\n")
        f.write("\tint reader_pos = 0;\n")

        index = 0
        indent_level = 1

        while index < len(tokens):
            token = tokens[index]

            if token.ttype == TokenType.increment:
                f.write("\t" * indent_level + f"reader_pos += {token.value};\n")
                index += 1
            if token.ttype == TokenType.decrement:
                f.write("\t" * indent_level + f"reader_pos -= {token.value};\n")
                index += 1
            if token.ttype == TokenType.plus:
                f.write(
                    "\t" * indent_level
                    + f"byte_array[reader_pos] = (byte_array[reader_pos] + {token.value}) % 256;\n"
                )
                index += 1
            if token.ttype == TokenType.minus:
                f.write(
                    "\t" * indent_level
                    + f"byte_array[reader_pos] = (byte_array[reader_pos] - {token.value}) % 256;\n"
                )
                index += 1
            if token.ttype == TokenType.dot:
                f.write("\t" * indent_level + 'printf("%c", byte_array[reader_pos]);\n')
                index += 1
            if token.ttype == TokenType.comma:
                f.write("\t" * indent_level + 'scanf("%d", byte_array[reader_pos]);\n')
            if token.ttype == TokenType.lbracket:
                f.write("\t" * indent_level + "while (byte_array[reader_pos]) {\n")
                indent_level += 1
                index += 1

            if token.ttype == TokenType.rbracket:
                indent_level -= 1
                f.write("\t" * indent_level + "}\n")
                index += 1

        f.write("}")


def print_usage():
    print("Usage:")
    print("\tProvide the path of the programan and the mode (sim, trans, comp).")
    print("\tFor example:")
    print("\t\t```$ python3 bf.py sim example/hello_world.bf```\n")
    print("\tAdditionally, you can enable debug mode with the `-debug=n` flag,")
    print("\twhere n is the number of cells from the byte array to print")
    print("\tFor example:")
    print("\t\t```$ python3 bf.py comp example/hello_world.bf -debug=10```\n")


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print_usage()

    file_path = ""
    debug = 0

    for arg in sys.argv:
        if "debug" in arg:
            debug = int(arg.split("=")[-1])
        if ".bf" in arg:
            file_path = arg
    assert len(file_path) > 0, "Please provide a file path."

    tokens = read_tokens(file_path)
    collapse_runs(tokens)
    cross_reference_porgram(tokens)

    if "sim" in sys.argv:
        simulate_program(tokens, debug)

    if "trans" in sys.argv:
        transpile_program(tokens)

    if "comp" in sys.argv:
        transpile_program(tokens)
        subprocess.run(["clang", "out.c", "-O3"])
        subprocess.run(["rm", "out.c"])


if __name__ == "__main__":
    main()
