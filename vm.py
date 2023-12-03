import math

from collections import deque

from Crypto.Hash import keccak


class Operation:
    def __init__(self, bytecode: str):
        # bytecode has to be even length
        if len(bytecode) == 0 or len(bytecode) % 2 != 0:
            raise Exception("Invalid bytecode length")

        # split into array of 2 characters
        self.parsed_bytecode = [bytecode[i:i+2] for i in range(0, len(bytecode), 2)]

        self.transaction = {}

        # pointer used to decide what opcode to step into next
        self.program_counter = 0

        self.stack = []

        self.memory = []

        self.storage = {}
        self.old_storage = {}

        self.logs = []
        self.old_logs = []

        self.return_bytes = None

        self.stopped = False

    def debug(self):
        print(f"bytecode: {''.join(self.parsed_bytecode)}")
        print(f"parsed_bytecode: {self.parsed_bytecode}")
        print(f"transaction: {self.transaction}")
        print(f"program_counter: {self.program_counter}")
        print(f"stack: {self.stack}")
        print(f"memory: {self.memory}")
        print(f"storage: {self.storage}")
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
            if b == 0:
                c = "0"
            else:
                c = hex(a // b)[2:]
            self.stack.append(c)
            self.program_counter += 1
            return

        # MOD
        elif opcode == "06":
            a = int(self.stack.pop(), 16)
            b = int(self.stack.pop(), 16)

            if b == 0:
                c = "0"
            else:
                c = hex(a % b)[2:]

            self.stack.append(c)
            self.program_counter += 1
            return

        # ADDMOD
        elif opcode == "08":
            a = int(self.stack.pop(), 16)
            b = int(self.stack.pop(), 16)
            c = int(self.stack.pop(), 16)

            if c == 0:
                d = "0"
            else:
                d = hex((a + b) % c)[2:]

            self.stack.append(d)
            self.program_counter += 1
            return

        # MULMOD
        elif opcode == "09":
            a = int(self.stack.pop(), 16)
            b = int(self.stack.pop(), 16)
            c = int(self.stack.pop(), 16)

            if c == 0:
                d = "0"
            else:
                d = hex((a * b) % c)[2:]

            self.stack.append(d)
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

        # AND
        elif opcode == "16":
            a = int(self.stack.pop(), 16)
            b = int(self.stack.pop(), 16)
            c = hex(a & b)[2:]
            self.stack.append(c)
            self.program_counter += 1
            return

        # OR
        elif opcode == "17":
            a = int(self.stack.pop(), 16)
            b = int(self.stack.pop(), 16)
            c = hex(a | b)[2:]
            self.stack.append(c)
            self.program_counter += 1
            return

        # XOR
        elif opcode == "18":
            a = int(self.stack.pop(), 16)
            b = int(self.stack.pop(), 16)
            c = hex(a ^ b)[2:]
            self.stack.append(c)
            self.program_counter += 1
            return

        # NOT
        elif opcode == "19":
            a = int(self.stack.pop(), 16)
            b = hex(~a & 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)[2:]
            self.stack.append(b)
            self.program_counter += 1
            return

        # BYTE
        elif opcode == "1a":
            offset = int(self.stack.pop(), 16)

            value = self.stack.pop().rjust(64, "0")
            value_byte_array = [value[idx:idx+2] for idx in range(0, len(value), 2)]
            try:
                byte = value_byte_array[offset]
            except IndexError:
                byte = "0"

            self.stack.append(byte)

            self.program_counter += 1
            return

        # SHL
        elif opcode == "1b":
            shift = int(self.stack.pop(), 16)
            value = int(self.stack.pop(), 16)

            shifted_value = hex((value << shift) & 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)[2:]
            self.stack.append(shifted_value)

            self.program_counter += 1
            return

        # SHR
        elif opcode == "1c":
            shift = int(self.stack.pop(), 16)
            value = int(self.stack.pop(), 16)

            shifted_value = hex((value >> shift) & 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)[2:]
            self.stack.append(shifted_value)

            self.program_counter += 1
            return

        # SHA3
        elif opcode == "20":
            offset = int(self.stack.pop(), 16)
            size = int(self.stack.pop(), 16)

            min_required_memory_size = math.ceil((offset + size) / 32) * 32
            if min_required_memory_size > len(self.memory):
                self.memory.extend(["00" for _ in range(min_required_memory_size - len(self.memory))])

            memory_bytes_array = []
            for idx in range(size):
                memory_byte = self.memory[idx + offset]
                memory_bytes_array.append(memory_byte)

            memory_bytes = "".join(memory_bytes_array)
            hashed_value = keccak.new(digest_bits=256, data=bytes.fromhex(memory_bytes)).hexdigest()

            self.stack.append(hashed_value)
            self.program_counter += 1
            return

        # CALLVALUE
        elif opcode == "34":
            call_value = hex(int(self.transaction["value"]))[2:]
            self.stack.append(call_value)
            self.program_counter += 1
            return

        # CALLDATALOAD
        elif opcode == "35":
            offset = int(self.stack.pop(), 16)

            calldata = self.transaction.get("data", "0x")[2:]
            parsed_calldata = [calldata[i:i + 2] for i in range(0, len(calldata), 2)]

            bytes_list = []
            for idx in range(32):
                try:
                    byte = parsed_calldata[idx + offset]
                except IndexError:
                    byte = "00"
                bytes_list.append(byte)

            load_bytes = hex(int("".join(bytes_list), 16))[2:]
            self.stack.append(load_bytes)

            self.program_counter += 1
            return

        # CALLDATASIZE
        elif opcode == "36":
            calldata = self.transaction.get("data", "0x")[2:]
            parsed_calldata = [calldata[i:i + 2] for i in range(0, len(calldata), 2)]
            calldata_size = hex(len(parsed_calldata))[2:]

            self.stack.append(calldata_size)

            self.program_counter += 1
            return

        # CALLDATACOPY
        elif opcode == "37":
            memory_offset = int(self.stack.pop(), 16)
            calldata_offset = int(self.stack.pop(), 16)
            size = int(self.stack.pop(), 16)

            calldata = self.transaction.get("data", "0x")[2:]
            parsed_calldata = [calldata[i:i + 2] for i in range(0, len(calldata), 2)]

            min_required_memory_size = math.ceil((memory_offset + size) / 32) * 32
            if min_required_memory_size > len(self.memory):
                self.memory.extend(["00" for _ in range(min_required_memory_size - len(self.memory))])

            for idx in range(size):
                try:
                    byte = parsed_calldata[idx + calldata_offset]
                except IndexError:
                    byte = "00"
                self.memory[idx + memory_offset] = byte

            self.program_counter += 1
            return

        # MLOAD
        elif opcode == "51":
            offset = int(self.stack.pop(), 16)

            min_required_memory_size = math.ceil((offset + 32) / 32) * 32
            if min_required_memory_size > len(self.memory):
                self.memory.extend(["00" for _ in range(min_required_memory_size - len(self.memory))])

            word_byte_array = []
            for idx in range(32):
                byte = self.memory[idx + offset]
                word_byte_array.append(byte)

            word = hex(int("".join(word_byte_array), 16))[2:]
            self.stack.append(word)

            self.program_counter += 1
            return

        # MSTORE
        elif opcode == "52":
            offset = int(self.stack.pop(), 16)

            min_required_memory_size = math.ceil((offset + 32) / 32) * 32
            if min_required_memory_size > len(self.memory):
                self.memory.extend(["00" for _ in range(min_required_memory_size - len(self.memory))])

            value = self.stack.pop()
            value = value.rjust(64, "0")
            value_byte_array = [value[idx:idx+2] for idx in range(0, len(value), 2)]

            for idx in range(32):
                self.memory[idx + offset] = value_byte_array[idx]

            self.program_counter += 1
            return

        # MSTORE8
        elif opcode == "53":
            offset = int(self.stack.pop(), 16)

            min_required_memory_size = math.ceil((offset + 1) / 32) * 32
            if min_required_memory_size > len(self.memory):
                self.memory.extend(["00" for _ in range(min_required_memory_size - len(self.memory))])

            value = self.stack.pop()
            value = value.rjust(64, "0")
            value_byte_array = [value[idx:idx+2] for idx in range(0, len(value), 2)]

            self.memory[offset] = value_byte_array[-1]

            self.program_counter += 1
            return

        # SLOAD
        elif opcode == "54":
            key = self.stack.pop()
            value = self.storage.get(key, "0")
            self.stack.append(value)
            self.program_counter += 1
            return

        # SSTORE
        elif opcode == "55":
            key = self.stack.pop()
            value = self.stack.pop()
            self.storage[key] = value
            self.program_counter += 1
            return

        # JUMP
        elif opcode == "56":
            new_program_counter = int(self.stack.pop(), 16)
            if self.parsed_bytecode[new_program_counter] != "5b":
                print("invalid JUMP")
                self.stopped = True
            else:
                self.program_counter = new_program_counter
            return

        # JUMPI
        elif opcode == "57":
            new_program_counter = int(self.stack.pop(), 16)
            condition = int(self.stack.pop(), 16)

            if condition != 0:
                if self.parsed_bytecode[new_program_counter] != "5b":
                    print("invalid JUMP")
                    self.stopped = True
                else:
                    self.program_counter = new_program_counter
            else:
                self.program_counter += 1
            return

        # JUMPDEST
        elif opcode == "5b":
            self.program_counter += 1
            return

        # PC
        elif opcode == "58":
            self.stack.append(str(self.program_counter))

            self.program_counter += 1
            return

        # MSIZE
        elif opcode == "59":
            memory_size = hex(len(self.memory))[2:]
            self.stack.append(memory_size)

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

        # DUP1 to DUP16
        elif opcode in {"80", "81", "82", "83", "84", "85", "86", "87",
                        "88", "89", "8a", "8b", "8c", "8d", "8e", "8f"}:
            self.program_counter += 1
            stack_item_reverse_index = int(opcode, 16) - 127
            stack_item = self.stack[-stack_item_reverse_index]
            self.stack.append(stack_item)
            return

        # SWAP1 to SWAP16
        elif opcode in {"90", "91", "92", "93", "94", "95", "96", "97",
                        "98", "99", "9a", "9b", "9c", "9d", "9e", "9f"}:
            self.program_counter += 1
            stack_item_a_reverse_index = -1
            stack_item_b_reverse_index = -(int(opcode, 16) - 142)
            self.stack[stack_item_a_reverse_index], self.stack[stack_item_b_reverse_index] = self.stack[stack_item_b_reverse_index], self.stack[stack_item_a_reverse_index]
            return

        # LOG0 to LOG4
        elif opcode in {"a0", "a1", "a2", "a3", "a4"}:
            offset = int(self.stack.pop(), 16)
            size = int(self.stack.pop(), 16)

            topics = {}
            num_of_topics = int(opcode[-1])
            for topic_num in range(num_of_topics):
                topics[f"topic{topic_num}"] = hex(int(self.stack.pop(), 16))

            min_required_memory_size = math.ceil((offset + size) / 32) * 32
            if min_required_memory_size > len(self.memory):
                self.memory.extend(["00" for _ in range(min_required_memory_size - len(self.memory))])

            data_byte_array = []
            for idx in range(size):
                byte = self.memory[idx + offset]
                data_byte_array.append(byte)
            data = hex(int("".join(data_byte_array), 16))

            log = {"data": data, **topics}
            self.logs.append(log)

            self.program_counter += 1
            return

        # CODESIZE
        elif opcode == "38":
            self.stack.append(hex(len(self.parsed_bytecode))[2:])
            self.program_counter += 1
            return

        # CODECOPY
        elif opcode == "39":
            memory_offset = int(self.stack.pop(), 16)
            bytecode_offset = int(self.stack.pop(), 16)
            size = int(self.stack.pop(), 16)

            min_required_memory_size = math.ceil((memory_offset + size) / 32) * 32
            if min_required_memory_size > len(self.memory):
                self.memory.extend(["00" for _ in range(min_required_memory_size - len(self.memory))])

            for idx in range(size):
                try:
                    bytecode_byte = self.parsed_bytecode[idx + bytecode_offset]
                except IndexError:
                    bytecode_byte = "00"
                self.memory[idx + memory_offset] = bytecode_byte

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

        # RETURN
        elif opcode == "f3":
            offset = int(self.stack.pop(), 16)
            size = int(self.stack.pop(), 16)

            min_required_memory_size = math.ceil((offset + size) / 32) * 32
            if min_required_memory_size > len(self.memory):
                self.memory.extend(["00" for _ in range(min_required_memory_size - len(self.memory))])

            return_bytes_array = []
            for idx in range(size):
                byte = self.memory[idx + offset]
                return_bytes_array.append(byte)

            return_bytes = "0x" + "".join(return_bytes_array)

            self.program_counter += 1
            self.stopped = True
            self.return_bytes = return_bytes

        # REVERT
        elif opcode == "fd":
            offset = int(self.stack.pop(), 16)
            size = int(self.stack.pop(), 16)

            min_required_memory_size = math.ceil((offset + size) / 32) * 32
            if min_required_memory_size > len(self.memory):
                self.memory.extend(["00" for _ in range(min_required_memory_size - len(self.memory))])

            return_bytes_array = []
            for idx in range(size):
                byte = self.memory[idx + offset]
                return_bytes_array.append(byte)

            return_bytes = "0x" + "".join(return_bytes_array)

            self.storage = self.old_storage
            self.logs = self.old_logs
            self.program_counter += 1
            self.stopped = True
            self.return_bytes = return_bytes

        # INVALID
        elif opcode == "fe":
            self.storage = self.old_storage
            self.logs = self.old_logs
            self.stopped = True
            self.program_counter += 1
            return

        else:
            print(f"OPCODE {opcode} not implemented")
            self.stopped = True
            return

    def execute(self, transaction):
        # calldata has to be even length if present
        if len(transaction.get("data", "0x")) % 2 != 0:
            raise Exception("Invalid calldata length")

        self.transaction = transaction

        self.stack = []
        self.memory = []
        self.old_storage = dict(self.storage)
        self.old_logs = list(self.old_logs)

        while not self.stopped:
            self.step()

        self.old_storage = {}
        self.old_logs = []
