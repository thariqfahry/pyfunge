# %%
import sys
import random

from instruction_set import instruction_dict, direction_dict

# A list-like object to act as Befunge's stack that returns 0 if popped
# while empty.
class BefungeStack(list):
    def pop(self):
        if self.__len__() == 0:
            return 0
        else:
            return super().pop()
    def __getitem__(self, index):
        raise RuntimeError("getitem should not be used!")
        # try:
        #     return super().__getitem__(index)
        # except IndexError:
        #     return 0

    def __setitem__(self, index, value):
        raise RuntimeError("setitem should not be used!")
        # try:
        #     super().__setitem__(index, value)
        # except IndexError:
        #     pass


class Interpreter:
    def __init__(self, raw_program: str) -> None:
        if not raw_program:
            self.error("Program empty.")

        # Convert program to a list of strings, one for each line.
        self.program = raw_program.splitlines()
        self.width = len(max(self.program))
        self.height = len(self.program)
        
        # Right-pad lines with whitespace to make program rectangular.
        self.program = [format(line, f'<{self.width}') for line in self.program]

        # Initialise instruction pointer, initial direction, string mode, 
        # and create empty stack.
        self.x, self.y = 0, 0
        self.direction = '>'
        self.string_mode = False
        self.stack = BefungeStack()

    def run(self):
        while True:
            self.execute_instruction()
            self.advance_pointer()

    def execute_instruction(self):
        instruction = self.program[self.y][self.x]
        # print(instruction,f" at {self.y},{self.x}")
        if self.string_mode and instruction != '"':
            self.stack.append(ord(instruction))
        else:
            try:
                instruction_dict[instruction](self)
            except KeyError:
                self.error(f"Syntax error: Unknown character: '{instruction}' ")

    def advance_pointer(self):
        direction_dict[self.direction](self)

    def error(self, message: str):
        print(f"\nError at l{self.y+1} c{self.x+1} going {self.direction}: ", message)
        self.terminate(-1)

    @staticmethod
    def terminate(exit_code: int):
        # print(f"\nProgram terminated with exit code: {exit_code}")
        sys.exit(exit_code)
