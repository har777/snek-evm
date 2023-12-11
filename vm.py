import math

from collections import deque
from enum import Enum

import rlp
from Crypto.Hash import keccak


class OperationStatus(Enum):
    EXECUTING = "EXECUTING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class Operation:
    def __init__(self, evm, address, transaction_metadata, operation_metadata):
        self.status = OperationStatus.EXECUTING

        self.evm = evm

        self.contract = evm.address_to_contract[address]
        bytecode = self.contract.bytecode

        # split into array of 2 characters
        self.parsed_bytecode = [bytecode[i:i+2] for i in range(0, len(bytecode), 2)]

        self.transaction_metadata = transaction_metadata
        self.operation_metadata = operation_metadata

        # pointer used to decide what opcode to step into next
        self.program_counter = 0

        self.stack = []
        self.memory = []

        self.old_nonce = self.contract.nonce
        self.old_storage = dict(self.contract.storage)
        self.old_logs = list(self.contract.logs)

        self.child_operations = []
        self.create_contracts = []

        self.return_bytes = ""

    def debug(self):
        print(f"contract: {self.contract}")
        print(f"parsed_bytecode: {self.parsed_bytecode}")
        print(f"program_counter: {self.program_counter}")
        print(f"transaction_metadata: {self.transaction_metadata}")
        print(f"operation_metadata: {self.operation_metadata}")
        print(f"stack: {self.stack}")
        print(f"memory: {self.memory}")
        print(f"status: {self.status}")
        print("\n")

    def step(self):
        if self.program_counter >= len(self.parsed_bytecode):
            self.status = OperationStatus.SUCCESS

        # code done executing
        if self.status in {OperationStatus.SUCCESS, OperationStatus.FAILURE}:
            return

        opcode = self.parsed_bytecode[self.program_counter]

        # STOP
        if opcode == "00":
            self.program_counter += 1
            # eh revisit
            self.status = OperationStatus.SUCCESS
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

        # EXP
        elif opcode == "0a":
            a = int(self.stack.pop(), 16)
            exponent = int(self.stack.pop(), 16)

            c = hex(pow(a, exponent, 2**256))[2:]

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

        # ADDRESS
        elif opcode == "30":
            self.stack.append(self.contract.address[2:])
            self.program_counter += 1
            return

        # ORIGIN
        elif opcode == "32":
            parent_operation = self
            while parent_operation.operation_metadata.parent_operation:
                parent_operation = parent_operation.operation_metadata.parent_operation

            self.stack.append(parent_operation.transaction_metadata.from_address[2:])
            self.program_counter += 1
            return

        # CALLER
        elif opcode == "33":
            self.stack.append(self.transaction_metadata.from_address[2:])
            self.program_counter += 1
            return

        # CALLVALUE
        elif opcode == "34":
            call_value = hex(int(self.transaction_metadata.value))[2:]
            self.stack.append(call_value)
            self.program_counter += 1
            return

        # CALLDATALOAD
        elif opcode == "35":
            offset = int(self.stack.pop(), 16)

            calldata = self.transaction_metadata.data[2:]
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
            calldata = self.transaction_metadata.data[2:]
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

            calldata = self.transaction_metadata.data[2:]
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
            value = self.contract.storage.get(key, "0")
            self.stack.append(value)
            self.program_counter += 1
            return

        # SSTORE
        elif opcode == "55":
            if self.operation_metadata.is_static_call_context:
                self.rollback()
                return

            key = self.stack.pop()
            value = self.stack.pop()
            self.contract.storage[key] = value
            self.program_counter += 1
            return

        # JUMP
        elif opcode == "56":
            new_program_counter = int(self.stack.pop(), 16)
            if self.parsed_bytecode[new_program_counter] != "5b":
                print("invalid JUMP")
                self.rollback()
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
                    self.rollback()
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
            if self.operation_metadata.is_static_call_context:
                self.rollback()
                return

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
            self.contract.logs.append(log)

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

        # EXTCODESIZE
        elif opcode == "3b":
            address = "0x" + self.stack.pop()
            external_contract = self.evm.address_to_contract[address]
            if not external_contract:
                self.stack.append("0")
            else:
                external_bytecode = external_contract.bytecode
                external_parsed_bytecode = [external_bytecode[i:i+2] for i in range(0, len(external_bytecode), 2)]
                code_size = hex(len(external_parsed_bytecode))[2:]
                self.stack.append(code_size)

            self.program_counter += 1
            return

        # EXTCODECOPY
        elif opcode == "3c":
            address = "0x" + self.stack.pop()
            memory_offset = int(self.stack.pop(), 16)
            bytecode_offset = int(self.stack.pop(), 16)
            size = int(self.stack.pop(), 16)

            min_required_memory_size = math.ceil((memory_offset + size) / 32) * 32
            if min_required_memory_size > len(self.memory):
                self.memory.extend(["00" for _ in range(min_required_memory_size - len(self.memory))])

            external_contract = self.evm.address_to_contract[address]
            external_bytecode = external_contract.bytecode if external_contract else ""
            external_parsed_bytecode = [external_bytecode[i:i + 2] for i in range(0, len(external_bytecode), 2)]

            for idx in range(size):
                try:
                    external_bytecode_byte = external_parsed_bytecode[idx + bytecode_offset]
                except IndexError:
                    external_bytecode_byte = "00"
                self.memory[idx + memory_offset] = external_bytecode_byte

            self.program_counter += 1
            return

        # RETURNDATASIZE
        elif opcode == "3d":
            if not self.child_operations:
                self.stack.append("0")
            else:
                return_bytes = self.child_operations[-1].return_bytes
                parsed_return_bytes = [return_bytes[i:i+2] for i in range(0, len(return_bytes), 2)]
                return_size = hex(len(parsed_return_bytes))[2:]
                self.stack.append(return_size)

            self.program_counter += 1
            return

        # RETURNDATACOPY
        elif opcode == "3e":
            memory_offset = int(self.stack.pop(), 16)
            return_bytes_offset = int(self.stack.pop(), 16)
            size = int(self.stack.pop(), 16)

            min_required_memory_size = math.ceil((memory_offset + size) / 32) * 32
            if min_required_memory_size > len(self.memory):
                self.memory.extend(["00" for _ in range(min_required_memory_size - len(self.memory))])

            if not self.child_operations:
                parsed_return_bytes = []
            else:
                return_bytes = self.child_operations[-1].return_bytes
                parsed_return_bytes = [return_bytes[i:i+2] for i in range(0, len(return_bytes), 2)]

            for idx in range(size):
                parsed_return_byte = parsed_return_bytes[idx + return_bytes_offset]
                self.memory[idx + memory_offset] = parsed_return_byte

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

        # CREATE
        elif opcode == "f0":
            if self.operation_metadata.is_static_call_context:
                self.rollback()
                return

            self.stack.pop()
            offset = int(self.stack.pop(), 16)
            size = int(self.stack.pop(), 16)

            min_required_memory_size = math.ceil((offset + size) / 32) * 32
            if min_required_memory_size > len(self.memory):
                self.memory.extend(["00" for _ in range(min_required_memory_size - len(self.memory))])

            create_bytecode = "".join(self.memory[offset:offset+size])
            create_address = get_create_contract_address(sender_address=self.contract.address, sender_nonce=self.contract.nonce)

            create_contract = self.evm.create_contract(bytecode=create_bytecode, address=create_address)
            operation = self.evm.execute_transaction(
                address=create_address,
                transaction_metadata=TransactionMetadata(from_address=self.contract.address),
                operation_metadata=OperationMetadata(is_static_call_context=self.operation_metadata.is_static_call_context, parent_operation=self)
            )
            if operation.status == OperationStatus.FAILURE:
                self.stack.append("0")
                del self.evm.address_to_contract[create_address]
            else:
                self.create_contracts.append(create_contract)
                self.contract.nonce += 1
                self.stack.append(create_address[2:])
                create_contract.bytecode = operation.return_bytes

            self.program_counter += 1

            return

        # CALL
        elif opcode == "f1":
            self.stack.pop()
            address = "0x" + self.stack.pop()
            value = self.stack.pop()
            args_offset = int(self.stack.pop(), 16)
            args_size = int(self.stack.pop(), 16)
            ret_offset = int(self.stack.pop(), 16)
            ret_size = int(self.stack.pop(), 16)

            if self.operation_metadata.is_static_call_context and value != 0:
                self.rollback()
                return

            min_required_memory_size = math.ceil((args_offset + args_size) / 32) * 32
            if min_required_memory_size > len(self.memory):
                self.memory.extend(["00" for _ in range(min_required_memory_size - len(self.memory))])

            operation_calldata = "0x" + "".join(self.memory[args_offset:args_offset+args_size])

            operation = self.evm.execute_transaction(
                address=address,
                transaction_metadata=TransactionMetadata(data=operation_calldata, from_address=self.contract.address),
                operation_metadata=OperationMetadata(is_static_call_context=self.operation_metadata.is_static_call_context, parent_operation=self)
            )

            self.child_operations.append(operation)
            if operation.status == OperationStatus.FAILURE:
                self.stack.append("0")
            else:
                min_required_memory_size = math.ceil((ret_offset + ret_size) / 32) * 32
                if min_required_memory_size > len(self.memory):
                    self.memory.extend(["00" for _ in range(min_required_memory_size - len(self.memory))])

                return_bytes_array = [operation.return_bytes[2:][i:i+2] for i in range(0, len(operation.return_bytes[2:]), 2)]
                for idx in range(ret_size):
                    byte = return_bytes_array[idx]
                    self.memory[idx + ret_offset] = byte

                self.stack.append("1")

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

            return_bytes = "".join(return_bytes_array)

            self.program_counter += 1
            self.status = OperationStatus.SUCCESS
            self.return_bytes = return_bytes

            return

        # CREATE2
        elif opcode == "f5":
            if self.operation_metadata.is_static_call_context:
                self.rollback()
                return

            self.stack.pop()
            offset = int(self.stack.pop(), 16)
            size = int(self.stack.pop(), 16)
            salt = int(self.stack.pop(), 16)

            min_required_memory_size = math.ceil((offset + size) / 32) * 32
            if min_required_memory_size > len(self.memory):
                self.memory.extend(["00" for _ in range(min_required_memory_size - len(self.memory))])

            create2_bytecode = "".join(self.memory[offset:offset+size])

            parent_operation = self
            while parent_operation.operation_metadata.parent_operation:
                parent_operation = parent_operation.operation_metadata.parent_operation
            origin_address = parent_operation.transaction_metadata.from_address

            create2_address = get_create2_contract_address(origin_address=origin_address, salt=salt, initialisation_code=create2_bytecode)

            if create2_address in self.evm.address_to_contract:
                self.stack.append("0")
            else:
                create2_contract = self.evm.create_contract(bytecode=create2_bytecode, address=create2_address)
                operation = self.evm.execute_transaction(
                    address=create2_address,
                    transaction_metadata=TransactionMetadata(from_address=self.contract.address),
                    operation_metadata=OperationMetadata(is_static_call_context=self.operation_metadata.is_static_call_context, parent_operation=self)
                )
                if operation.status == OperationStatus.FAILURE:
                    self.stack.append("0")
                    del self.evm.address_to_contract[create2_address]
                else:
                    self.create_contracts.append(create2_contract)
                    self.contract.nonce += 1
                    self.stack.append(create2_address[2:])
                    create2_contract.bytecode = operation.return_bytes

            self.program_counter += 1

            return

        # STATICCALL
        elif opcode == "fa":
            self.stack.pop()
            address = "0x" + self.stack.pop()
            args_offset = int(self.stack.pop(), 16)
            args_size = int(self.stack.pop(), 16)
            ret_offset = int(self.stack.pop(), 16)
            ret_size = int(self.stack.pop(), 16)

            min_required_memory_size = math.ceil((args_offset + args_size) / 32) * 32
            if min_required_memory_size > len(self.memory):
                self.memory.extend(["00" for _ in range(min_required_memory_size - len(self.memory))])

            operation_calldata = "0x" + "".join(self.memory[args_offset:args_offset + args_size])

            operation = self.evm.execute_transaction(
                address=address,
                transaction_metadata=TransactionMetadata(data=operation_calldata, from_address=self.contract.address),
                operation_metadata=OperationMetadata(is_static_call_context=True, parent_operation=self)
            )

            self.child_operations.append(operation)
            if operation.status == OperationStatus.FAILURE:
                self.stack.append("0")
            else:
                min_required_memory_size = math.ceil((ret_offset + ret_size) / 32) * 32
                if min_required_memory_size > len(self.memory):
                    self.memory.extend(["00" for _ in range(min_required_memory_size - len(self.memory))])

                return_bytes_array = [operation.return_bytes[2:][i:i + 2] for i in
                                      range(0, len(operation.return_bytes[2:]), 2)]
                for idx in range(ret_size):
                    byte = return_bytes_array[idx]
                    self.memory[idx + ret_offset] = byte

                self.stack.append("1")

            self.program_counter += 1
            return

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

            self.rollback()
            self.return_bytes = return_bytes

            return

        # INVALID
        elif opcode == "fe":
            self.rollback()
            return

        else:
            print(f"OPCODE {opcode} not implemented")
            self.rollback()
            return

    def rollback(self):
        for child_operation in reversed(self.child_operations):
            child_operation.rollback()

        for create_contract in self.create_contracts:
            create_address = create_contract.address
            del self.evm.address_to_contract[create_address]

        self.contract.nonce = self.old_nonce
        self.contract.storage = self.old_storage
        self.contract.logs = self.old_logs
        self.status = OperationStatus.FAILURE

    def execute(self, debug=False):
        try:
            if debug:
                self.debug()
            while self.status == OperationStatus.EXECUTING:
                self.step()
                if debug:
                    self.debug()
        except Exception as e:
            self.rollback()
            raise e


class Contract:
    def __init__(self, bytecode, address):
        self.bytecode = bytecode.lower()
        self.address = address.lower()
        self.nonce = 0
        self.storage = {}
        self.logs = []

    def __str__(self):
        return f"Contract(bytecode={self.bytecode}, address={self.address}, nonce={self.nonce} storage={self.storage}, logs={self.logs})"


class TransactionMetadata:
    def __init__(self, from_address, value="0", data="0x"):
        # calldata has to be even length if present
        if len(data) % 2 != 0:
            raise Exception("Invalid calldata length")

        self.from_address = from_address.lower()
        self.value = value
        self.data = data.lower()

    def __str__(self):
        return f"TransactionMetadata(from={self.from_address} value={self.value}, data={self.data})"


class OperationMetadata:
    def __init__(self, is_static_call_context=False, parent_operation=None):
        self.is_static_call_context = is_static_call_context
        self.parent_operation = parent_operation

    def __str__(self):
        return f"OperationMetadata(is_static_call_context={self.is_static_call_context}, parent_operation={self.parent_operation})"


class EVM:
    def __init__(self):
        self.address_to_contract = {}

    def create_contract(self, bytecode, address):
        contract = Contract(bytecode=bytecode, address=address)
        self.address_to_contract[address] = contract
        return contract

    def execute_transaction(self, address, transaction_metadata, operation_metadata=None, debug=False):
        if not operation_metadata:
            operation_metadata = OperationMetadata()

        operation = Operation(
            evm=self,
            address=address,
            transaction_metadata=transaction_metadata,
            operation_metadata=operation_metadata,
        )
        operation.execute(debug=debug)
        return operation

    def __str__(self):
        return f"EVM(address_to_contract={self.address_to_contract})"


def get_create_contract_address(sender_address: str, sender_nonce: int):
    sender = bytes.fromhex(sender_address[2:])
    contract_address = "0x" + keccak.new(digest_bits=256, data=rlp.encode([sender, sender_nonce])).hexdigest()[-40:]
    return contract_address


def get_create2_contract_address(origin_address: str, salt: int, initialisation_code: str):
    contract_address = "0x" + keccak.new(digest_bits=256, data=(
            bytes.fromhex("ff") +
            bytes.fromhex(origin_address[2:]) +
            bytes.fromhex(hex(salt)[2:].rjust(64, "0")) +
            bytes.fromhex(keccak.new(digest_bits=256, data=bytes.fromhex(initialisation_code)).hexdigest())
    )).hexdigest()[-40:]
    return contract_address
