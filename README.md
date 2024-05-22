## This is yet another Brainfuck emulator
A [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck) interpreter written in Python.

### Quick Brainfuck intro
The following are the only operations allowed in Brainfuck, every othern character in a Brainfuck source file is considered comment, and is ignored.

- **>** = increment the memory pointer, in other words, move the pointer to the right by 1.
- **<** = decrement the memory pointer, in other words, move the pointer to the left by 1.
- **+** = increases value stored at the cell pointed to by the memory pointer
- **-** = decreases value stored at the cell pointed to by the memory pointer
- **[** = loop while the stored value in the current cell is not 0
- **]** = jump back to the last preceding opening bracket for the loop
- **,** = read and store a byte in the current cell
- **.** = output the stored value of the current cell

*Note:* The input and output in Brainfuck is ASCII encoded, so if you want to write and 'a' you have to write *97*.

### Quickstart
Try out some of the examples in the *examples/* directory by running the following command in your terminal:
```console
$ python3 bf.py examples/hello_world.bf
```

You can even see what the byte array looks like at each step by running the program with the `-debug` flag like this:
```console
$ python3 bf.py examples/hello_world.bf -debug=10
```

### Where next?
The next step is to have the option to compile to x86-64 assembly.
