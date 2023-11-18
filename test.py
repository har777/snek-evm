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
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600a600a01'_
        # PUSH1 0x0a
        # PUSH1 0x0a
        # ADD
        contract = Contract(bytecode="600a600a01")
        contract.execute()
        self.assertEqual(contract.stack, ["14"])

    def test_mul(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600a600a02'_
        # PUSH1 0x0a
        # PUSH1 0x0a
        # MUL
        contract = Contract(bytecode="600a600a02")
        contract.execute()
        self.assertEqual(contract.stack, ["64"])

    def test_sub(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600a600a03'_
        # PUSH1 0x0a
        # PUSH1 0x0a
        # SUB
        contract = Contract(bytecode="600a600a03")
        contract.execute()
        self.assertEqual(contract.stack, ["0"])

    def test_div(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600a600a04'_
        # PUSH1 0x0a
        # PUSH1 0x0a
        # DIV
        contract = Contract(bytecode="600a600a04")
        contract.execute()
        self.assertEqual(contract.stack, ["1"])

    def test_lt(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600a600910600a600a10'_
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
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='6009600a11600a600a11'_
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
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600a600a146005600a14'_
        # PUSH1 0x0a
        # PUSH1 0x0a
        # EQ
        # PUSH1 0x05
        # PUSH1 0x0a
        # EQ
        contract = Contract(bytecode="600a600a146005600a14")
        contract.execute()
        self.assertEqual(contract.stack, ["1", "0"])
