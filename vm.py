from collections import deque


class Contract:
    def __init__(self, bytecode: str):
        # bytecode has to be even length
        if len(bytecode) == 0 or len(bytecode) % 2 != 0:
            raise Exception("Invalid bytecode length")

        # split into array of 2 characters
        self.parsed_bytecode = [bytecode[i:i+2] for i in range(0, len(bytecode), 2)]

        # pointer used to decide what opcode to step into next
        self.program_counter = 0

        self.stack = []

        self.stopped = False

    def debug(self):
        print(f"bytecode: {''.join(self.parsed_bytecode)}")
        print(f"parsed_bytecode: {self.parsed_bytecode}")
        print(f"program_counter: {self.program_counter}")
        print(f"stack: {self.stack}")
        print(f"stopped: {self.stopped}")

    def step(self):
        if self.program_counter >= len(self.parsed_bytecode):
            self.stopped = True

        # code done executing
        if self.stopped:
            return

        opcode = self.parsed_bytecode[self.program_counter]

        raise Exception(f"OPCODE {opcode} not implemented")

    def execute(self):
        while not self.stopped:
            self.step()
