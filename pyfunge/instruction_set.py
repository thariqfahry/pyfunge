import random
import sys

direction_dict = {
    '>': lambda self: setattr(self, 'x', (self.x+1) % (self.width )),
    '<': lambda self: setattr(self, 'x', (self.x-1) % (self.width )),
    '^': lambda self: setattr(self, 'y', (self.y-1) % (self.height)),
    'v': lambda self: setattr(self, 'y', (self.y+1) % (self.height))
    }

instruction_dict = {}

# No-op
instruction_dict[' '] = lambda self: None

# Integers
def append_numeric(number):
    def wrapper(self):
        self.stack.append(number)
    return wrapper

for number in range(0,10):
    instruction_dict[str(number)] = append_numeric(number)

# Arithmetic #TODO minimum 2 check / OOB
def add(self):
    self.stack.append(self.stack.pop() + self.stack.pop())
instruction_dict['+'] = add

def subtract(self):
    a = self.stack.pop()
    b = self.stack.pop()
    self.stack.append(b-a)
instruction_dict['-'] = subtract

def multiply(self):
    self.stack.append(self.stack.pop() * self.stack.pop())    
instruction_dict['*'] = multiply

def divide(self):
    a = self.stack.pop()
    b = self.stack.pop()
    self.stack.append(b//a)
instruction_dict['/'] = divide

# Actually a remainder operation! The Befunge-93 spec just calls it 'modulo'.
def modulo(self):
    a = self.stack.pop()
    b = self.stack.pop()
    self.stack.append(b-(round(b/a)*a))
instruction_dict['%'] = modulo

# Logical
def logical_not(self):
    self.stack.append(1 if self.stack.pop() == 0 else 0)
instruction_dict['!'] = logical_not

# Conditional
def greater_than(self):
    a = self.stack.pop()
    b = self.stack.pop()
    self.stack.append(1 if b > a else 0)
instruction_dict['`'] = greater_than

# Direction change
def change_direction(direction):
    def wrapper(self):
        self.direction = direction
    return wrapper

for direction in ['>','<','^','v']:
    instruction_dict[direction] = change_direction(direction)

def random_direction(self):
    self.direction = random.choice(['>','<','^','v'])
instruction_dict['?'] = random_direction

def horizontal_if(self):
    self.direction = '>' if self.stack.pop() == 0 else '<'
instruction_dict['_'] = horizontal_if

def vertical_if(self):
    self.direction = 'v' if self.stack.pop() == 0 else '^'
instruction_dict['|'] = vertical_if

# String mode
def string_mode_toggle(self):
    self.string_mode = not self.string_mode
instruction_dict['"'] = string_mode_toggle

# Stack manipulation
def duplicate(self):
    a = self.stack.pop()
    self.stack.append(a)
    self.stack.append(a)
instruction_dict[':'] = duplicate

def swap(self):
    a = self.stack.pop()
    b = self.stack.pop()
    self.stack.append(a)
    self.stack.append(b)
instruction_dict['\\'] = swap

def pop(self):
    self.stack.pop()
instruction_dict['$'] = pop

# Standard output
def print_int(self):
    sys.stdout.write(str(self.stack.pop()) + ' ')
instruction_dict['.'] = print_int

def print_ascii(self):
    sys.stdout.write(chr(self.stack.pop()))
instruction_dict[','] = print_ascii

# Skip cell
def bridge(self):
    self.advance_pointer()
instruction_dict['#'] = bridge

# Program manipulation
def put(self):
    y = self.stack.pop()
    x = self.stack.pop()
    v = self.stack.pop()

    line = list(self.program[y])
    line[x] = chr(v)
    self.program[y] = "".join(line)
instruction_dict['p'] = put

def get(self):
    y = self.stack.pop()
    x = self.stack.pop()

    self.stack.append(ord(self.program[y][x]))
instruction_dict['g'] = get

# Input
def integer_input(self):
    integer = input()
    if not integer.isnumeric():
        self.error("Invalid input. Input must be a number.")
    self.stack.append(int(integer))
instruction_dict['&'] = integer_input

def character_input(self):
    character = input()
    if len(character) != 1:
        self.error("Invalid input. Input must be a single character.")
    self.stack.append(ord(character))
instruction_dict['~'] = character_input

# def end_program(self):
#     self.terminate(0)
# instruction_dict['@'] = end_program
