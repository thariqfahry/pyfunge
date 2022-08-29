from interpreter import Interpreter
import os
import sys

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = "pyfunge",
        description = "Run a Befunge-93 file"
    )

    parser.add_argument(
        "Filename",
        type = str,
        metavar = 'filename',
        help = "The Befunge file to run"
    )

    args = parser.parse_args()

    if not os.path.exists(args.Filename):
        print(f"{args.Filename} does not exist.")
        sys.exit(-1)

    with open(args.Filename) as f:
        interp = Interpreter(f.read())
        interp.run()