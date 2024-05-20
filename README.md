## This is yet another Brainfuck emulator
A [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck) interpreter written in Python.

### Quickstart
Try out some of the examples in the *examples/* directory by running the following command in your terminal:
```console
$ python3 bf.py examples/hello_world.bf
```

You can even see what the byte array looks like at each step by running the program with the `-debug` flag like this:
```console
$ python3 bf.py examples/hello_world.bf -debug
```

### Where next?
The next step is to have the option to compile to x86-64 assembly.
