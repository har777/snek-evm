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

        # ADD a b
        elif opcode == "01":
            a = int(self.stack.pop(), 16)
            b = int(self.stack.pop(), 16)
            c = hex((a + b) % 2**256)[2:]
            self.stack.append(c)
            self.program_counter += 1
            return

        # MUL a b
        elif opcode == "02":
            a = int(self.stack.pop(), 16)
            b = int(self.stack.pop(), 16)
            c = hex((a * b) % 2**256)[2:]
            self.stack.append(c)
            self.program_counter += 1
            return

        # SUB a b
        elif opcode == "03":
            a = int(self.stack.pop(), 16)
            b = int(self.stack.pop(), 16)
            c = hex((a - b) % 2**256)[2:]
            self.stack.append(c)
            self.program_counter += 1
            return

        # DIV a b
        elif opcode == "04":
            a = int(self.stack.pop(), 16)
            b = int(self.stack.pop(), 16)
            c = hex(a // b)[2:]
            self.stack.append(c)
            self.program_counter += 1
            return

        # LT a b
        elif opcode == "10":
            a = int(self.stack.pop(), 16)
            b = int(self.stack.pop(), 16)
            c = "1" if a < b else "0"
            self.stack.append(c)
            self.program_counter += 1
            return

        # GT a b
        elif opcode == "11":
            a = int(self.stack.pop(), 16)
            b = int(self.stack.pop(), 16)
            c = "1" if a > b else "0"
            self.stack.append(c)
            self.program_counter += 1
            return

        # EQ a b
        elif opcode == "14":
            a = int(self.stack.pop(), 16)
            b = int(self.stack.pop(), 16)
            c = "1" if a == b else "0"
            self.stack.append(c)
            self.program_counter += 1
            return

        # ISZERO
        elif opcode == "15":
            a = int(self.stack.pop(), 16)
            b = "1" if a == 0 else "0"
            self.stack.append(b)
            self.program_counter += 1
            return

        # PUSH0
        elif opcode == "5f":
            self.stack.append("0")
            self.program_counter += 1
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

        # CODESIZE
        elif opcode == "38":
            self.stack.append(hex(len(self.parsed_bytecode))[2:])
            self.program_counter += 1
            return

        # GASLIMIT
        elif opcode == "45":
            self.stack.append("ffffffffffff")
            self.program_counter += 1
            return

        # CHAINID
        elif opcode == "46":
            self.stack.append("1")
            self.program_counter += 1
            return

        # BASEFEE
        elif opcode == "48":
            self.stack.append("a")
            self.program_counter += 1
            return

        # POP
        elif opcode == "50":
            self.stack.pop()
            self.program_counter += 1
            return

        raise Exception(f"OPCODE {opcode} not implemented")

    def execute(self):
        while not self.stopped:
            self.step()
