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

        # STOP
        if opcode == "00":
            self.program_counter += 1
            self.stopped = True
            return

        # PUSH0
        elif opcode == "5f":
            self.program_counter += 1
            self.stack.append("0")
            return

        # PUSH1 to PUSH32
        elif opcode in {"60", "61", "62", "63", "64", "65", "66", "67",
                        "68", "69", "6a", "6b", "6c", "6d", "6e", "6f",
                        "70", "71", "72", "73", "74", "75", "76", "77",
                        "78", "79", "7a", "7b", "7c", "7d", "7e", "7f"}:
            self.program_counter += 1
            num_of_bytes = int(opcode, 16) - 95

            bytes_list = deque([])
            for _ in range(num_of_bytes):
                try:
                    val = self.parsed_bytecode[self.program_counter]
                    bytes_list.append(val)
                    self.program_counter += 1
                except IndexError:
                    val = "00"
                    bytes_list.appendleft(val)
            bytes_num = hex(int("".join(bytes_list), 16))[2:]
            self.stack.append(bytes_num)
            return

        raise Exception(f"OPCODE {opcode} not implemented")

    def execute(self):
        while not self.stopped:
            self.step()
