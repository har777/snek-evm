import unittest

from vm import EVM, TransactionMetadata, get_create_contract_address


class UtilTestCase(unittest.TestCase):
    def test_get_create_contract_address(self):
        sender_address = "0x6ac7ea33f8831ea9dcc53393aaa88b25a785dbf0"

        self.assertEqual(get_create_contract_address(sender_address=sender_address, sender_nonce=0),
                         "0xcd234a471b72ba2f1ccf0a70fcaba648a5eecd8d")
        self.assertEqual(get_create_contract_address(sender_address=sender_address, sender_nonce=1),
                         "0x343c43a37d37dff08ae8c4a11544c718abb4fcf8")
        self.assertEqual(get_create_contract_address(sender_address=sender_address, sender_nonce=2),
                         "0xf778b86fa74e846c4f0a1fbd1335fe81c00a0c91")
        self.assertEqual(get_create_contract_address(sender_address=sender_address, sender_nonce=3),
                         "0xfffd933a0bc612844eaf0c6fe3e5b8e9b6c1d19c")


class OpcodeTestCase(unittest.TestCase):
    def setUp(self):
        self.evm = EVM()
        self.address_1 = "0xd8da6bf26964af9d7eed9e03e53415d37aa96045"
        self.address_2 = "0xd8da6bf26964af9d7eed9e03e53415d37aa96046"
        self.eoa_1 = "0xd8da6bf26964af9d7eed9e03e53415d37aa96047"

    def test_stop(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600a00600a'_
        # PUSH1 0x0a
        # STOP
        # PUSH1 0x0a
        self.evm.create_contract(bytecode="600a00600a", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["a"])

    def test_push0(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='5f5f'_
        # PUSH0
        # PUSH0
        self.evm.create_contract(bytecode="5f5f", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["0", "0"])

    def test_push1(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='60ff6000'_
        # PUSH1 0xff
        # PUSH1 0x00
        self.evm.create_contract(bytecode="60ff6000", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["ff", "0"])

    def test_push31(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7eyyyyyw7exxxxxv'~wwwzvvvy~~xzzwffv00%01vwxyz~_
        # PUSH31 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        # PUSH31 0x00000000000000000000000000000000000000000000000000000000000000
        self.evm.create_contract(
            bytecode="7effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7e00000000000000000000000000000000000000000000000000000000000000", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "0"])

        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7ezzzzz7e7e0a'~ffffffz~~%01z~_
        # PUSH31 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7e
        # PUSH31 0x0a
        self.evm.create_contract(bytecode="7effffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7e7e0a", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7e", "a"])

    def test_push32(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f0000000000000000000000000000000000000000000000000000000000000000'_
        # PUSH32 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        # PUSH32 0x0000000000000000000000000000000000000000000000000000000000000000
        self.evm.create_contract(
            bytecode="7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f0000000000000000000000000000000000000000000000000000000000000000", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "0"])

    def test_dup1(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600180'_
        # PUSH1 0x01
        # DUP1
        self.evm.create_contract(bytecode="600180", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["1", "1"])

    def test_dup2(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='6001600081'_
        # PUSH1 0x01
        # PUSH1 0x00
        # DUP2
        self.evm.create_contract(bytecode="6001600081", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["1", "0", "1"])

    def test_dup15(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='z1~~~~~~~8e'~z0z0z600%01z~_
        # PUSH1 0x01
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # DUP15
        self.evm.create_contract(bytecode="6001600060006000600060006000600060006000600060006000600060008e", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack,
                         ["1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1"])

    def test_dup16(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='z1~~~~~8f'~z0z0z0z600%01z~_
        # PUSH1 0x01
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # DUP16
        self.evm.create_contract(bytecode="60016000600060006000600060006000600060006000600060006000600060008f", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack,
                         ["1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1"])

    def test_swap1(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='6002600190'_
        # PUSH1 0x02
        # PUSH1 0x01
        # SWAP1
        self.evm.create_contract(bytecode="6002600190", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["1", "2"])

    def test_swap2(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='60026000600191'_
        # PUSH1 0x02
        # PUSH1 0x00
        # PUSH1 0x01
        # SWAP2
        self.evm.create_contract(bytecode="60026000600191", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["1", "0", "2"])

    def test_swap15(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='z2~~~~~~~z19e'~z0z0z600%01z~_
        # PUSH1 0x02
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x01
        # SWAP15
        self.evm.create_contract(bytecode="60026000600060006000600060006000600060006000600060006000600060019e", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack,
                         ["1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "2"])

    def test_swap16(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='z2~~~~~z19f'~z0z0z0z600%01z~_
        # PUSH1 0x02
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x01
        # SWAP16
        self.evm.create_contract(bytecode="600260006000600060006000600060006000600060006000600060006000600060019f", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack,
                         ["1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "2"])

    def test_codesize(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7cyyyyz5038'~zzz0z00y~~%01yz~_
        # PUSH29 0x0000000000000000000000000000000000000000000000000000000000
        # POP
        # CODESIZE
        self.evm.create_contract(bytecode="7c00000000000000000000000000000000000000000000000000000000005038", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["20"])

    def test_codecopy(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7dxxxxx7fwwww505060206y6y396008601f6y39'~yy00zffffffy000xzzw~~%01wxyz~_
        # PUSH30 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        # PUSH32 0x0000000000000000000000000000000000000000000000000000000000000000
        # POP
        # POP
        # PUSH1 0x20
        # PUSH1 0x00
        # PUSH1 0x00
        # CODECOPY
        # PUSH1 0x08
        # PUSH1 0x1f
        # PUSH1 0x00
        # CODECOPY
        self.evm.create_contract(bytecode="7dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f00000000000000000000000000000000000000000000000000000000000000005050602060006000396008601f600039", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, [])
        self.assertEqual("".join(operation.memory), "7f00000000000000ffffffffffffffffffffffffffffffffffffffffffffff7f")

    def test_extcodesize(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7f7vvvx527wx526020xf3yyyyy06020526029xxf03b'~wwfz000yzzzx6zwfffv~~~%01vwxyz~_
        # PUSH32 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        # PUSH1 0x00
        # MSTORE
        # PUSH32 0xff60005260206000f30000000000000000000000000000000000000000000000
        # PUSH1 0x20
        # MSTORE
        # PUSH1 0x29
        # PUSH1 0x00
        # PUSH1 0x00
        # CREATE
        # EXTCODESIZE
        self.evm.create_contract(bytecode="7f7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff6000527fff60005260206000f30000000000000000000000000000000000000000000000602052602960006000f03b", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["20"])
        self.assertEqual("".join(operation.memory), "7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff60005260206000f30000000000000000000000000000000000000000000000")

    def test_extcodecopy(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7f7sssv7uvxyf3wwwww0x52r29yyf0yvyx52xytr08r1ft'~000zuufy6~xr20w~~~vy52ufffty833cszzzr60%01rstuvwxyz~_
        # PUSH32 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        # PUSH1 0x00
        # MSTORE
        # PUSH32 0xff60005260206000f30000000000000000000000000000000000000000000000
        # PUSH1 0x20
        # MSTORE
        # PUSH1 0x29
        # PUSH1 0x00
        # PUSH1 0x00
        # CREATE
        # PUSH1 0x00
        # PUSH1 0x00
        # MSTORE
        # PUSH1 0x00
        # PUSH1 0x20
        # MSTORE
        # PUSH1 0x20
        # PUSH1 0x00
        # PUSH1 0x00
        # DUP4
        # EXTCODECOPY
        # PUSH1 0x08
        # PUSH1 0x1f
        # PUSH1 0x00
        # DUP4
        # EXTCODECOPY
        self.evm.create_contract(bytecode="7f7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff6000527fff60005260206000f30000000000000000000000000000000000000000000000602052602960006000f060006000526000602052602060006000833c6008601f6000833c", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, [operation.create_contracts[0].address[2:]])
        self.assertEqual("".join(operation.memory), "ff00000000000000ffffffffffffffffffffffffffffffffffffffffffffffff0000000000000000000000000000000000000000000000000000000000000000")

    def test_returndatasize(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7f7f7rrrrrft7wt7wtv0uvs7fy0vsv9u00604s604dxxf0xxxx8463zwa3d'~000zwwy~~~x6~wfffv602uxf3yyyytx52s052rzz%01rstuvwxyz~_
        # PUSH32 0x7f7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        # PUSH1 0x00
        # MSTORE
        # PUSH32 0xff6000527fff60005260206000f3000000000000000000000000000000000000
        # PUSH1 0x20
        # MSTORE
        # PUSH32 0x000000000060205260296000f300000000000000000000000000000000000000
        # PUSH1 0x40
        # MSTORE
        # PUSH1 0x4d
        # PUSH1 0x00
        # PUSH1 0x00
        # CREATE
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # DUP5
        # PUSH4 0xffffffff
        # STATICCALL
        # RETURNDATASIZE
        self.evm.create_contract(bytecode="7f7f7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff6000527fff6000527fff60005260206000f30000000000000000000000000000000000006020527f000000000060205260296000f300000000000000000000000000000000000000604052604d60006000f060006000600060008463fffffffffa3d", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["3e4ea2156166390f880071d94458efb098473311", "1", "20"])
        self.assertEqual("".join(operation.memory), "7f7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff6000527fff60005260206000f3000000000000000000000000000000000000000000000060205260296000f300000000000000000000000000000000000000")

    def test_returndatacopy(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7f7f7qqqqqfppyvwswv7fx0wvt29s00t40vt4drf0rr8463zua5050rvywvyt40vwr3et01t1fw3e'~000zuuy6~x~~~wt20v52uffft60syf3xxxxryyqzzpyv7u%01pqrstuvwxyz~_
        # PUSH32 0x7f7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        # PUSH1 0x00
        # MSTORE
        # PUSH32 0xff6000527fff60005260206000f3000000000000000000000000000000000000
        # PUSH1 0x20
        # MSTORE
        # PUSH32 0x000000000060205260296000f300000000000000000000000000000000000000
        # PUSH1 0x40
        # MSTORE
        # PUSH1 0x4d
        # PUSH1 0x00
        # PUSH1 0x00
        # CREATE
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # DUP5
        # PUSH4 0xffffffff
        # STATICCALL
        # POP
        # POP
        # PUSH1 0x00
        # PUSH1 0x00
        # MSTORE
        # PUSH1 0x00
        # PUSH1 0x20
        # MSTORE
        # PUSH1 0x00
        # PUSH1 0x40
        # MSTORE
        # PUSH1 0x20
        # PUSH1 0x00
        # PUSH1 0x00
        # RETURNDATACOPY
        # PUSH1 0x01
        # PUSH1 0x1f
        # PUSH1 0x20
        # RETURNDATACOPY
        self.evm.create_contract(bytecode="7f7f7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff6000527fff6000527fff60005260206000f30000000000000000000000000000000000006020527f000000000060205260296000f300000000000000000000000000000000000000604052604d60006000f060006000600060008463fffffffffa50506000600052600060205260006040526020600060003e6001601f60203e", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, [])
        self.assertEqual("".join(operation.memory), "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")

    def test_gaslimit(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='45'_
        # GASLIMIT
        self.evm.create_contract(bytecode="45", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["ffffffffffff"])

    def test_chainid(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='46'_
        # CHAINID
        self.evm.create_contract(bytecode="46", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["1"])

    def test_basefee(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='48'_
        # BASEFEE
        contract = self.evm.create_contract(bytecode="48", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["a"])

    def test_pop(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='6201ec2150'_
        # PUSH3 0x01ec21
        # POP
        self.evm.create_contract(bytecode="6201ec2150", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, [])

    def test_add(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600a600a017yyyyf600101'~zzzzzffy~~%01yz~_
        # PUSH1 0x0a
        # PUSH1 0x0a
        # ADD
        # PUSH32 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        # PUSH1 0x01
        # ADD
        self.evm.create_contract(
            bytecode="600a600a017fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff600101", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["14", "0"])

    def test_mul(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600a600a027yyyyf600202'~zzzzzffy~~%01yz~_
        # PUSH1 0x0a
        # PUSH1 0x0a
        # MUL
        # PUSH32 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        # PUSH1 0x02
        # MUL
        self.evm.create_contract(
            bytecode="600a600a027fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff600202", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["64", "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe"])

    def test_sub(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='~a~a03~1~003'~600%01~_
        # PUSH1 0x0a
        # PUSH1 0x0a
        # SUB
        # PUSH1 0x01
        # PUSH1 0x00
        # SUB
        self.evm.create_contract(bytecode="600a600a036001600003", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["0", "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"])

    def test_div(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='~a~a04~2~104'~600%01~_
        # PUSH1 0x0a
        # PUSH1 0x0a
        # DIV
        # PUSH1 0x02
        # PUSH1 0x01
        # DIV
        contract = self.evm.create_contract(bytecode="600a600a046002600104", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["1", "0"])

    def test_mod(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='6003600a066005601106'_
        # PUSH1 0x03
        # PUSH1 0x0a
        # MOD
        # PUSH1 0x05
        # PUSH1 0x11
        # MOD
        self.evm.create_contract(bytecode="6003600a066005601106", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["1", "2"])

    def test_addmod(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='z8zaza08z2z27xxxxf08'~yyyyz600yffx~~%01xyz~_
        # PUSH1 0x08
        # PUSH1 0x0a
        # PUSH1 0x0a
        # ADDMOD
        # PUSH1 0x02
        # PUSH1 0x02
        # PUSH32 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        # ADDMOD
        self.evm.create_contract(bytecode="6008600a600a08600260027fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff08", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["4", "1"])

    def test_mulmod(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='z8zaza09zc7xx~7xx~09'~yyyyfz600yfffx~~%01xyz~_
        # PUSH1 0x08
        # PUSH1 0x0a
        # PUSH1 0x0a
        # MULMOD
        # PUSH1 0x0c
        # PUSH32 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        # PUSH32 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        # MULMOD
        self.evm.create_contract(bytecode="6008600a600a09600c7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff09", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["4", "9"])

    def test_lt(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='~a~910~a~a10'~600%01~_
        # PUSH1 0x0a
        # PUSH1 0x09
        # LT
        # PUSH1 0x0a
        # PUSH1 0x0a
        # LT
        self.evm.create_contract(bytecode="600a600910600a600a10", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["1", "0"])

    def test_gt(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='~9~a11~a~a11'~600%01~_
        # PUSH1 0x09
        # PUSH1 0x0a
        # GT
        # PUSH1 0x0a
        # PUSH1 0x0a
        # GT
        self.evm.create_contract(bytecode="6009600a11600a600a11", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["1", "0"])

    def test_eq(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='~a~a14~5~a14'~600%01~_
        # PUSH1 0x0a
        # PUSH1 0x0a
        # EQ
        # PUSH1 0x05
        # PUSH1 0x0a
        # EQ
        self.evm.create_contract(bytecode="600a600a146005600a14", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["1", "0"])

    def test_iszero(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600a15600015'_
        # PUSH1 0x0a
        # ISZERO
        # PUSH1 0x00
        # ISZERO
        self.evm.create_contract(bytecode="600a15600015", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["0", "1"])

    def test_and(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600f600f16600060ff16'_
        # PUSH1 0x0f
        # PUSH1 0x0f
        # AND
        # PUSH1 0x00
        # PUSH1 0xff
        # AND
        self.evm.create_contract(bytecode="600f600f16600060ff16", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["f", "0"])

    def test_or(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600f60f01760ff60ff17'_
        # PUSH1 0x0f
        # PUSH1 0xf0
        # OR
        # PUSH1 0xff
        # PUSH1 0xff
        # OR
        self.evm.create_contract(bytecode="600f60f01760ff60ff17", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["ff", "ff"])

    def test_xor(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600f60f01860ff60ff18'_
        # PUSH1 0x0f
        # PUSH1 0xf0
        # XOR
        # PUSH1 0xff
        # PUSH1 0xff
        # XOR
        self.evm.create_contract(bytecode="600f60f01860ff60ff18", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["ff", "0"])

    def test_not(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='6000196001197yyf197~f00y~z00~19'~zzzffffy~~~~%01yz~_
        # PUSH1 0x00
        # NOT
        # PUSH1 0x01
        # NOT
        # PUSH32 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        # NOT
        # PUSH32 0xffffffff00ffffffffffffffffffffffffffffffffffffffffffff00ffffffff
        # NOT
        self.evm.create_contract(bytecode="6000196001197fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
                                     "ffff197fffffffff00ffffffffffffffffffffffffffffffffffffffffffff00ffffffff19", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(
            operation.stack,
            [
                "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe",
                "0",
                "ff00000000000000000000000000000000000000000000ff00000000"
            ]
        )

    def test_byte(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='60ff601f1a61ff00601e1a60ff60201a'_
        # PUSH1 0xff
        # PUSH1 0x1f
        # BYTE
        # PUSH2 0xff00
        # PUSH1 0x1e
        # BYTE
        # PUSH1 0xff
        # PUSH1 0x20
        # BYTE
        self.evm.create_contract(bytecode="60ff601f1a61ff00601e1a60ff60201a", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["ff", "ff", "0"])

    def test_shl(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='6z16z11b7fffyyyyyz6z41b'~zzzz00y~~%01yz~_
        # PUSH1 0x01
        # PUSH1 0x01
        # SHL
        # PUSH32 0xff00000000000000000000000000000000000000000000000000000000000000
        # PUSH1 0x04
        # SHL
        self.evm.create_contract(bytecode="600160011b7fff0000000000000000000000000000000000000000000000000000000000000060041b", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["2", "f000000000000000000000000000000000000000000000000000000000000000"])

    def test_shr(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600260011c60ff60041c'_
        # PUSH1 0x02
        # PUSH1 0x01
        # SHR
        # PUSH1 0xff
        # PUSH1 0x04
        # SHR
        self.evm.create_contract(bytecode="600260011c60ff60041c", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["1", "f"])

    def test_sload(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='602e600055600054600154'_
        # PUSH1 0x2e
        # PUSH1 0x00
        # SSTORE
        # PUSH1 0x00
        # SLOAD
        # PUSH1 0x01
        # SLOAD
        contract = self.evm.create_contract(bytecode="602e600055600054600154", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["2e", "0"])
        self.assertEqual(contract.storage, {"0": "2e"})

    def test_sstore(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='61ffff6000556100ff61230555'_
        # PUSH2 0xffff
        # PUSH1 0x00
        # SSTORE
        # PUSH2 0x00ff
        # PUSH2 0x2305
        # SSTORE
        contract = self.evm.create_contract(bytecode="61ffff6000556100ff61230555", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, [])
        self.assertEqual(contract.storage, {"0": "ffff", "2305": "ff"})

    def test_mstore(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='~052~152'~60ff600%01~_
        # PUSH1 0xff
        # PUSH1 0x00
        # MSTORE
        # PUSH1 0xff
        # PUSH1 0x01
        # MSTORE
        self.evm.create_contract(bytecode="60ff60005260ff600152", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, [])
        self.assertEqual("".join(operation.memory), "0000000000000000000000000000000000000000000000000000000000000000ff00000000000000000000000000000000000000000000000000000000000000")

    def test_mstore8(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='61ffee60005360ff600153'_
        # PUSH2 0xffee
        # PUSH1 0x00
        # MSTORE8
        # PUSH1 0xff
        # PUSH1 0x01
        # MSTORE8
        self.evm.create_contract(bytecode="61ffee60005360ff600153", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, [])
        self.assertEqual("".join(operation.memory), "eeff000000000000000000000000000000000000000000000000000000000000")

    def test_mload(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7fyyyyyzff6z0526z0516z151'~zzzz00y~~%01yz~_
        # PUSH32 0x00000000000000000000000000000000000000000000000000000000000000ff
        # PUSH1 0x00
        # MSTORE
        # PUSH1 0x00
        # MLOAD
        # PUSH1 0x01
        # MLOAD
        self.evm.create_contract(bytecode="7f00000000000000000000000000000000000000000000000000000000000000ff600052600051600151", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["ff", "ff00"])
        self.assertEqual("".join(operation.memory), "00000000000000000000000000000000000000000000000000000000000000ff0000000000000000000000000000000000000000000000000000000000000000")

    def test_msize(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='5960005150596039515059'_
        # MSIZE
        # PUSH1 0x00
        # MLOAD
        # POP
        # MSIZE
        # PUSH1 0x39
        # MLOAD
        # POP
        # MSIZE
        self.evm.create_contract(bytecode="5960005150596039515059", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["0", "20", "60"])
        self.assertEqual("".join(operation.memory), "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")

    def test_jumpdest(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='5b5b'_
        # JUMPDEST
        # JUMPDEST
        self.evm.create_contract(bytecode="5b5b", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, [])

    def test_jump(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600456fe5b6001'_
        # PUSH1 0x04
        # JUMP
        # INVALID
        # JUMPDEST
        # PUSH1 0x01
        self.evm.create_contract(bytecode="600456fe5b6001", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["1"])

    def test_jumpi(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='~0~a57~1~c575bfe5b~1'~600%01~_
        # PUSH1 0x00
        # PUSH1 0x0a
        # JUMPI
        # PUSH1 0x01
        # PUSH1 0x0c
        # JUMPI
        # JUMPDEST
        # INVALID
        # JUMPDEST
        # PUSH1 0x01
        self.evm.create_contract(bytecode="6000600a576001600c575bfe5b6001", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["1"])

    def test_pc(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='58585b58600158'_
        # PC
        # PC
        # JUMPDEST
        # PC
        # PUSH1 0x01
        # PC
        self.evm.create_contract(bytecode="58585b58600158", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["0", "1", "3", "1", "6"])

    def test_callvalue(self):
        # https://www.evm.codes/playground?fork=shanghai&callValue=123456789&unit=Wei&codeType=Bytecode&code='34'_
        # CALLVALUE
        self.evm.create_contract(bytecode="34", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(value="123456789", from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["75bcd15"])

    def test_calldataload(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&callData=0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff&codeType=Bytecode&code=%27600035601f35%27_
        # PUSH1 0x00
        # CALLDATALOAD
        # PUSH1 0x1f
        # CALLDATALOAD
        self.evm.create_contract(bytecode="600035601f35", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(data="0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", from_address=self.eoa_1))
        self.assertEqual(operation.stack, [
            "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            "ff00000000000000000000000000000000000000000000000000000000000000",
        ])

    def test_calldatasize(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&callData=0xff&codeType=Bytecode&code=%2736%27_
        # CALLDATASIZE
        self.evm.create_contract(bytecode="36", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(data="0xff", from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["1"])

    def test_calldatacopy(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&callData=0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff&codeType=Bytecode&code=%276020%7E0%7E037%7E8601f%7E037%27%7E600%01%7E_
        # PUSH1 0x20
        # PUSH1 0x00
        # PUSH1 0x00
        # CALLDATACOPY
        # PUSH1 0x08
        # PUSH1 0x1f
        # PUSH1 0x00
        # CALLDATACOPY
        self.evm.create_contract(bytecode="602060006000376008601f600037", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(data="0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", from_address=self.eoa_1))
        self.assertEqual(operation.stack, [])
        self.assertEqual("".join(operation.memory), "ff00000000000000ffffffffffffffffffffffffffffffffffffffffffffffff")

    def test_log0(self):
        # PUSH1 0xff
        # PUSH1 0x00
        # MSTORE
        # PUSH1 0x20
        # PUSH1 0x00
        # LOG0
        contract = self.evm.create_contract(bytecode="60ff60005260206000a0", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, [])
        self.assertEqual(contract.logs, [{"data": "0xff"}])

    def test_log1(self):
        # PUSH1 0xff
        # PUSH1 0x00
        # MSTORE
        # PUSH32 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
        # PUSH1 0x20
        # PUSH1 0x00
        # LOG1
        contract = self.evm.create_contract(bytecode="60ff6000527fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef60206000a1", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, [])
        self.assertEqual(contract.logs, [{
            "data": "0xff",
            "topic0": "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
        }])

    def test_log2(self):
        # PUSH1 0xff
        # PUSH1 0x00
        # MSTORE
        # PUSH32 0xbae7ebe87fc708426a193f49c4829cdc6221ac84
        # PUSH32 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
        # PUSH1 0x20
        # PUSH1 0x00
        # LOG2
        contract = self.evm.create_contract(bytecode="60ff6000527f000000000000000000000000bae7ebe87fc708426a193f49c4829cdc6221ac847fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef60206000a2", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, [])
        self.assertEqual(contract.logs, [{
            "data": "0xff",
            "topic0": "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
            "topic1": "0xbae7ebe87fc708426a193f49c4829cdc6221ac84",
        }])

    def test_log3(self):
        # PUSH1 0xff
        # PUSH1 0x00
        # MSTORE
        # PUSH32 0x4f6742badb049791cd9a37ea913f2bac38d01279
        # PUSH32 0xbae7ebe87fc708426a193f49c4829cdc6221ac84
        # PUSH32 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
        # PUSH1 0x20
        # PUSH1 0x00
        # LOG3
        contract = self.evm.create_contract(bytecode="60ff6000527f0000000000000000000000004f6742badb049791cd9a37ea913f2bac38d012797f000000000000000000000000bae7ebe87fc708426a193f49c4829cdc6221ac847fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef60206000a3", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, [])
        self.assertEqual(contract.logs, [{
            "data": "0xff",
            "topic0": "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
            "topic1": "0xbae7ebe87fc708426a193f49c4829cdc6221ac84",
            "topic2": "0x4f6742badb049791cd9a37ea913f2bac38d01279",
        }])

    def test_log4(self):
        # PUSH1 0xff
        # PUSH1 0x00
        # MSTORE
        # PUSH16 0x2ccc2087078963d621f42338ab0
        # PUSH32 0x4f6742badb049791cd9a37ea913f2bac38d01279
        # PUSH32 0xbae7ebe87fc708426a193f49c4829cdc6221ac84
        # PUSH32 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
        # PUSH1 0x3c
        # PUSH1 0x00
        # LOG4
        contract = self.evm.create_contract(bytecode="60ff6000526f000002ccc2087078963d621f42338ab07f0000000000000000000000004f6742badb049791cd9a37ea913f2bac38d012797f000000000000000000000000bae7ebe87fc708426a193f49c4829cdc6221ac847fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef603c6000a4", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, [])
        self.assertEqual(contract.logs, [{
            "data": "0xff00000000000000000000000000000000000000000000000000000000",
            "topic0": "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
            "topic1": "0xbae7ebe87fc708426a193f49c4829cdc6221ac84",
            "topic2": "0x4f6742badb049791cd9a37ea913f2bac38d01279",
            "topic3": "0x2ccc2087078963d621f42338ab0",
        }])

    def test_return(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef6z527fyyyyy00226zf3'~zzz000y~~%01yz~_
        # PUSH32 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
        # PUSH1 0x00
        # MSTORE
        # PUSH32 0x0000000000000000000000000000000000000000000000000000000000000022
        # PUSH1 0x00
        # RETURN
        self.evm.create_contract(bytecode="7fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef6000527f00000000000000000000000000000000000000000000000000000000000000226000f3", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, [])
        self.assertEqual("".join(operation.memory), "ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef0000000000000000000000000000000000000000000000000000000000000000")
        self.assertEqual(operation.return_bytes, "ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef0000")

    def test_sha3(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7fffffffffyyyy6z5260046z20'~zz0z000y~~%01yz~_
        # PUSH32 0xffffffff00000000000000000000000000000000000000000000000000000000
        # PUSH1 0x00
        # MSTORE
        # PUSH1 0x04
        # PUSH1 0x00
        # SHA3
        self.evm.create_contract(bytecode="7fffffffff000000000000000000000000000000000000000000000000000000006000526004600020", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["29045a592007d0c246ef02c2223570da9522d0cf0f73282c79a1bc8f0bb2c238"])
        self.assertEqual("".join(operation.memory), "ffffffff00000000000000000000000000000000000000000000000000000000")

    def test_address(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='30'_
        # ADDRESS
        self.evm.create_contract(bytecode="30", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, [self.address_1[2:]])

    def test_origin(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='32'_
        # ORIGIN
        self.evm.create_contract(bytecode="32", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, [self.eoa_1[2:]])

    def test_caller(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='33'_
        # CALLER
        self.evm.create_contract(bytecode="33", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, [self.eoa_1[2:]])

    def test_invalid(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='6100ff61230555fe6001'_
        # PUSH2 0x00ff
        # PUSH2 0x2305
        # SSTORE
        # INVALID
        # PUSH1 0x01
        contract = self.evm.create_contract(bytecode="6100ff61230555fe6001", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, [])
        self.assertEqual(contract.storage, {})
        self.assertEqual("".join(operation.memory), "")

    def test_revert(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='6042600052602060006100ff61230555fd6042'_
        # PUSH1 0x42
        # PUSH1 0x00
        # MSTORE
        # PUSH1 0x20
        # PUSH1 0x00
        # PUSH2 0x00ff
        # PUSH2 0x2305
        # SSTORE
        # REVERT
        # PUSH1 0x42
        contract = self.evm.create_contract(bytecode="6042600052602060006100ff61230555fd6042", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, [])
        self.assertEqual("".join(operation.memory), "0000000000000000000000000000000000000000000000000000000000000042")
        self.assertEqual(contract.storage, {})
        self.assertEqual(operation.return_bytes, "0x0000000000000000000000000000000000000000000000000000000000000042")

    def test_call(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600035600757fe5b'_
        # PUSH1 0x00
        # CALLDATALOAD
        # PUSH1 0x07
        # JUMPI
        # INVALID
        # JUMPDEST
        self.evm.create_contract(bytecode="600035600757fe5b", address=self.address_1)

        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='zzw~yf1zzx2~y7067z35w757fe5bz52w8x18f3z52f1'~0zz73d8da6bf26964af9d7eed9e03e53415d37aa9xzw0y4561ffffx60wx0%01wxyz~_
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH20 0xd8da6bf26964af9d7eed9e03e53415d37aa96045
        # PUSH2 0xffff
        # CALL
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x20
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH20 0xd8da6bf26964af9d7eed9e03e53415d37aa96045
        # PUSH2 0xffff
        # PUSH17 0x67600035600757fe5b60005260086018f3
        # PUSH1 0x00
        # MSTORE
        # CALL
        self.evm.create_contract(bytecode="6000600060006000600073d8da6bf26964af9d7eed9e03e53415d37aa9604561fffff16000600060206000600073d8da6bf26964af9d7eed9e03e53415d37aa9604561ffff7067600035600757fe5b60005260086018f3600052f1", address=self.address_2)

        operation = self.evm.execute_transaction(address=self.address_2, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["0", "1"])
        self.assertEqual("".join(operation.memory), "00000000000000000000000000000067600035600757fe5b60005260086018f3")
        self.assertEqual(operation.return_bytes, "")

    def test_staticcall(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7f7f7rrrrrft7wt7wtv0uvs7fy0vsv9u00604s604dxxf0xxxx8463zwa'~000zwwy~~~x6~wfffv602uxf3yyyytx52s052rzz%01rstuvwxyz~_
        # PUSH32 0x7f7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        # PUSH1 0x00
        # MSTORE
        # PUSH32 0xff6000527fff60005260206000f3000000000000000000000000000000000000
        # PUSH1 0x20
        # MSTORE
        # PUSH32 0x000000000060205260296000f300000000000000000000000000000000000000
        # PUSH1 0x40
        # MSTORE
        # PUSH1 0x4d
        # PUSH1 0x00
        # PUSH1 0x00
        # CREATE
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # DUP5
        # PUSH4 0xffffffff
        # STATICCALL
        self.evm.create_contract(bytecode="7f7f7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff6000527fff6000527fff60005260206000f30000000000000000000000000000000000006020527f000000000060205260296000f300000000000000000000000000000000000000604052604d60006000f060006000600060008463fffffffffa", address=self.address_1)

        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))
        self.assertEqual(operation.stack, ["3e4ea2156166390f880071d94458efb098473311", "1"])
        self.assertEqual("".join(operation.memory), "7f7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff6000527fff60005260206000f3000000000000000000000000000000000000000000000060205260296000f300000000000000000000000000000000000000")
        self.assertEqual(operation.return_bytes, "")

    def test_create(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='~x~~z9f06c63ffffffffy4601cf3ydx'~z0z600y~52zx~~f0%01xyz~_
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # CREATE
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x09
        # CREATE
        # PUSH13 0x63ffffffff6000526004601cf3
        # PUSH1 0x00
        # MSTORE
        # PUSH1 0x0d
        # PUSH1 0x13
        # PUSH1 0x00
        # CREATE
        contract = self.evm.create_contract(bytecode="600060006000f0600060006009f06c63ffffffff6000526004601cf3600052600d60136000f0", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))

        created_contract_1_address = get_create_contract_address(sender_address=self.address_1, sender_nonce=0)
        created_contract_2_address = get_create_contract_address(sender_address=self.address_1, sender_nonce=1)
        created_contract_3_address = get_create_contract_address(sender_address=self.address_1, sender_nonce=2)

        self.assertEqual(operation.stack, [created_contract_1_address[2:], created_contract_2_address[2:], created_contract_3_address[2:]])
        self.assertEqual("".join(operation.memory), "0000000000000000000000000000000000000063ffffffff6000526004601cf3")

        self.assertEqual(self.evm.address_to_contract[created_contract_1_address].bytecode, "")
        self.assertEqual(self.evm.address_to_contract[created_contract_2_address].bytecode, "")
        self.assertEqual(self.evm.address_to_contract[created_contract_3_address].bytecode, "ffffffff")

        self.assertEqual(contract.nonce, 3)

        # parent context fails -> check if all created contracts get deleted
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='~~yz9f06c63ffffffffx4601cf3xd6013yfd'~z0z600y~f0~~x~52z%01xyz~_
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # CREATE
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x09
        # CREATE
        # PUSH13 0x63ffffffff6000526004601cf3
        # PUSH1 0x00
        # MSTORE
        # PUSH1 0x0d
        # PUSH1 0x13
        # PUSH1 0x00
        # CREATE
        # PUSH1 0x00
        # PUSH1 0x00
        # REVERT
        self.evm = EVM()

        contract = self.evm.create_contract(bytecode="600060006000f0600060006009f06c63ffffffff6000526004601cf3600052600d60136000f060006000fd", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))

        created_contract_1_address = get_create_contract_address(sender_address=self.address_1, sender_nonce=0)
        created_contract_2_address = get_create_contract_address(sender_address=self.address_1, sender_nonce=1)
        created_contract_3_address = get_create_contract_address(sender_address=self.address_1, sender_nonce=2)

        self.assertEqual(operation.stack, [created_contract_1_address[2:], created_contract_2_address[2:], created_contract_3_address[2:]])
        self.assertEqual("".join(operation.memory), "0000000000000000000000000000000000000063ffffffff6000526004601cf3")

        self.assertEqual(self.evm.address_to_contract.get(created_contract_1_address, None), None)
        self.assertEqual(self.evm.address_to_contract.get(created_contract_2_address, None), None)
        self.assertEqual(self.evm.address_to_contract.get(created_contract_3_address, None), None)

        self.assertEqual(contract.nonce, 0)

        # 3rd child context fails -> check if 1st, 2nd and 4th CREATE calls are successful
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='~~x~~y09f0yfez1y1fx6c63ffffffffz4y1cf3zdy13x'~y00z~52y0y60x~f0%01xyz~_
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x00
        # CREATE
        # PUSH1 0x00
        # PUSH1 0x00
        # PUSH1 0x09
        # CREATE
        # PUSH1 0xfe
        # PUSH1 0x00
        # MSTORE
        # PUSH1 0x01
        # PUSH1 0x1f
        # PUSH1 0x00
        # CREATE
        # PUSH13 0x63ffffffff6000526004601cf3
        # PUSH1 0x00
        # MSTORE
        # PUSH1 0x0d
        # PUSH1 0x13
        # PUSH1 0x00
        # CREATE
        self.evm = EVM()

        contract = self.evm.create_contract(bytecode="600060006000f0600060006009f060fe6000526001601f6000f06c63ffffffff6000526004601cf3600052600d60136000f0", address=self.address_1)
        operation = self.evm.execute_transaction(address=self.address_1, transaction_metadata=TransactionMetadata(from_address=self.eoa_1))

        created_contract_1_address = get_create_contract_address(sender_address=self.address_1, sender_nonce=0)
        created_contract_2_address = get_create_contract_address(sender_address=self.address_1, sender_nonce=1)
        created_contract_3_address = get_create_contract_address(sender_address=self.address_1, sender_nonce=2)
        created_contract_4_address = get_create_contract_address(sender_address=self.address_1, sender_nonce=3)

        self.assertEqual(operation.stack, [created_contract_1_address[2:], created_contract_2_address[2:], "0", created_contract_3_address[2:]])
        self.assertEqual("".join(operation.memory), "0000000000000000000000000000000000000063ffffffff6000526004601cf3")

        self.assertEqual(self.evm.address_to_contract[created_contract_1_address].bytecode, "")
        self.assertEqual(self.evm.address_to_contract[created_contract_2_address].bytecode, "")
        self.assertEqual(self.evm.address_to_contract[created_contract_3_address].bytecode, "ffffffff")
        self.assertEqual(self.evm.address_to_contract.get(created_contract_4_address, None), None)

        self.assertEqual(contract.nonce, 3)
