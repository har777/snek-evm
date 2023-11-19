import unittest

from vm import Contract


class ContractTestCase(unittest.TestCase):
    def test_stop(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600a00600a'_
        # PUSH1 0x0a
        # STOP
        # PUSH1 0x0a
        contract = Contract(bytecode="600a00600a")
        contract.execute()
        self.assertEqual(contract.stack, ["a"])

    def test_push0(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='5f5f'_
        # PUSH0
        # PUSH0
        contract = Contract(bytecode="5f5f")
        contract.execute()
        self.assertEqual(contract.stack, ["0", "0"])

    def test_push1(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='60ff6000'_
        # PUSH1 0xff
        # PUSH1 0x00
        contract = Contract(bytecode="60ff6000")
        contract.execute()
        self.assertEqual(contract.stack, ["ff", "0"])

    def test_push31(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7eyyyyyw7exxxxxv'~wwwzvvvy~~xzzwffv00%01vwxyz~_
        # PUSH31 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        # PUSH31 0x00000000000000000000000000000000000000000000000000000000000000
        contract = Contract(bytecode="7effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7e00000000000000000000000000000000000000000000000000000000000000")
        contract.execute()
        self.assertEqual(contract.stack, ["ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "0"])

        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7ezzzzz7e7e0a'~ffffffz~~%01z~_
        # PUSH31 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7e
        # PUSH31 0x0a
        contract = Contract(bytecode="7effffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7e7e0a")
        contract.execute()
        self.assertEqual(contract.stack, ["ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7e", "a"])

    def test_push32(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f0000000000000000000000000000000000000000000000000000000000000000'_
        # PUSH32 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        # PUSH32 0x0000000000000000000000000000000000000000000000000000000000000000
        contract = Contract(bytecode="7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f0000000000000000000000000000000000000000000000000000000000000000")
        contract.execute()
        self.assertEqual(contract.stack, ["ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "0"])

    def test_dup1(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600180'_
        # PUSH1 0x01
        # DUP1
        contract = Contract(bytecode="600180")
        contract.execute()
        self.assertEqual(contract.stack, ["1", "1"])

    def test_dup2(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='6001600081'_
        # PUSH1 0x01
        # PUSH1 0x00
        # DUP2
        contract = Contract(bytecode="6001600081")
        contract.execute()
        self.assertEqual(contract.stack, ["1", "0", "1"])

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
        contract = Contract(bytecode="6001600060006000600060006000600060006000600060006000600060008e")
        contract.execute()
        self.assertEqual(contract.stack, ["1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1"])

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
        contract = Contract(bytecode="60016000600060006000600060006000600060006000600060006000600060008f")
        contract.execute()
        self.assertEqual(contract.stack, ["1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1"])

    def test_codesize(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7cyyyyz5038'~zzz0z00y~~%01yz~_
        # PUSH29 0x0000000000000000000000000000000000000000000000000000000000
        # POP
        # CODESIZE
        contract = Contract(bytecode="7c00000000000000000000000000000000000000000000000000000000005038")
        contract.execute()
        self.assertEqual(contract.stack, ["20"])

    def test_gaslimit(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='45'_
        # GASLIMIT
        contract = Contract(bytecode="45")
        contract.execute()
        self.assertEqual(contract.stack, ["ffffffffffff"])

    def test_chainid(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='46'_
        # CHAINID
        contract = Contract(bytecode="46")
        contract.execute()
        self.assertEqual(contract.stack, ["1"])

    def test_basefee(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='48'_
        # BASEFEE
        contract = Contract(bytecode="48")
        contract.execute()
        self.assertEqual(contract.stack, ["a"])

    def test_pop(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='6201ec2150'_
        # PUSH3 0x01ec21
        # POP
        contract = Contract(bytecode="6201ec2150")
        contract.execute()
        self.assertEqual(contract.stack, [])

    def test_add(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600a600a017yyyyf600101'~zzzzzffy~~%01yz~_
        # PUSH1 0x0a
        # PUSH1 0x0a
        # ADD
        # PUSH32 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        # PUSH1 0x01
        # ADD
        contract = Contract(bytecode="600a600a017fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff600101")
        contract.execute()
        self.assertEqual(contract.stack, ["14", "0"])

    def test_mul(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600a600a027yyyyf600202'~zzzzzffy~~%01yz~_
        # PUSH1 0x0a
        # PUSH1 0x0a
        # MUL
        # PUSH32 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        # PUSH1 0x02
        # MUL
        contract = Contract(bytecode="600a600a027fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff600202")
        contract.execute()
        self.assertEqual(contract.stack, ["64", "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe"])

    def test_sub(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='~a~a03~1~003'~600%01~_
        # PUSH1 0x0a
        # PUSH1 0x0a
        # SUB
        # PUSH1 0x01
        # PUSH1 0x00
        # SUB
        contract = Contract(bytecode="600a600a036001600003")
        contract.execute()
        self.assertEqual(contract.stack, ["0", "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"])

    def test_div(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='~a~a04~2~104'~600%01~_
        # PUSH1 0x0a
        # PUSH1 0x0a
        # DIV
        # PUSH1 0x02
        # PUSH1 0x01
        # DIV
        contract = Contract(bytecode="600a600a046002600104")
        contract.execute()
        self.assertEqual(contract.stack, ["1", "0"])

    def test_lt(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='~a~910~a~a10'~600%01~_
        # PUSH1 0x0a
        # PUSH1 0x09
        # LT
        # PUSH1 0x0a
        # PUSH1 0x0a
        # LT
        contract = Contract(bytecode="600a600910600a600a10")
        contract.execute()
        self.assertEqual(contract.stack, ["1", "0"])

    def test_gt(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='~9~a11~a~a11'~600%01~_
        # PUSH1 0x09
        # PUSH1 0x0a
        # GT
        # PUSH1 0x0a
        # PUSH1 0x0a
        # GT
        contract = Contract(bytecode="6009600a11600a600a11")
        contract.execute()
        self.assertEqual(contract.stack, ["1", "0"])

    def test_eq(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='~a~a14~5~a14'~600%01~_
        # PUSH1 0x0a
        # PUSH1 0x0a
        # EQ
        # PUSH1 0x05
        # PUSH1 0x0a
        # EQ
        contract = Contract(bytecode="600a600a146005600a14")
        contract.execute()
        self.assertEqual(contract.stack, ["1", "0"])

    def test_iszero(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600a15600015'_
        # PUSH1 0x0a
        # ISZERO
        # PUSH1 0x00
        # ISZERO
        contract = Contract(bytecode="600a15600015")
        contract.execute()
        self.assertEqual(contract.stack, ["0", "1"])

    def test_and(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600f600f16600060ff16'_
        # PUSH1 0x0f
        # PUSH1 0x0f
        # AND
        # PUSH1 0x00
        # PUSH1 0xff
        # AND
        contract = Contract(bytecode="600f600f16600060ff16")
        contract.execute()
        self.assertEqual(contract.stack, ["f", "0"])

    def test_or(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600f60f01760ff60ff17'_
        # PUSH1 0x0f
        # PUSH1 0xf0
        # OR
        # PUSH1 0xff
        # PUSH1 0xff
        # OR
        contract = Contract(bytecode="600f60f01760ff60ff17")
        contract.execute()
        self.assertEqual(contract.stack, ["ff", "ff"])

    def test_xor(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600f60f01860ff60ff18'_
        # PUSH1 0x0f
        # PUSH1 0xf0
        # XOR
        # PUSH1 0xff
        # PUSH1 0xff
        # XOR
        contract = Contract(bytecode="600f60f01860ff60ff18")
        contract.execute()
        self.assertEqual(contract.stack, ["ff", "0"])

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
        contract = Contract(bytecode="6000196001197fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
                                     "ffff197fffffffff00ffffffffffffffffffffffffffffffffffffffffffff00ffffffff19")
        contract.execute()
        self.assertEqual(
            contract.stack,
            [
                "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe",
                "0",
                "ff00000000000000000000000000000000000000000000ff00000000"
            ]
        )
