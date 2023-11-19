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

    def test_gaslimit(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='45'_
        # GASLIMIT
        contract = Contract(bytecode="45")
        contract.execute()
        self.assertEqual(contract.stack, ["ffffffffffff"])

    def test_basefee(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='48'_
        # BASEFEE
        contract = Contract(bytecode="48")
        contract.execute()
        self.assertEqual(contract.stack, ["a"])

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
