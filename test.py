import unittest

from vm import Contract


class ContractTestCase(unittest.TestCase):
    def test_stop(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600a00600a'_
        # PUSH1 0x0a
        # STOP
        # PUSH1 0x0a
        contract = Contract(bytecode="600a00600a")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["a"])

    def test_push0(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='5f5f'_
        # PUSH0
        # PUSH0
        contract = Contract(bytecode="5f5f")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["0", "0"])

    def test_push1(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='60ff6000'_
        # PUSH1 0xff
        # PUSH1 0x00
        contract = Contract(bytecode="60ff6000")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["ff", "0"])

    def test_push31(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7eyyyyyw7exxxxxv'~wwwzvvvy~~xzzwffv00%01vwxyz~_
        # PUSH31 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        # PUSH31 0x00000000000000000000000000000000000000000000000000000000000000
        contract = Contract(
            bytecode="7effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7e00000000000000000000000000000000000000000000000000000000000000")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "0"])

        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7ezzzzz7e7e0a'~ffffffz~~%01z~_
        # PUSH31 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7e
        # PUSH31 0x0a
        contract = Contract(bytecode="7effffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7e7e0a")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7e", "a"])

    def test_push32(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f0000000000000000000000000000000000000000000000000000000000000000'_
        # PUSH32 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        # PUSH32 0x0000000000000000000000000000000000000000000000000000000000000000
        contract = Contract(
            bytecode="7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f0000000000000000000000000000000000000000000000000000000000000000")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "0"])

    def test_dup1(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600180'_
        # PUSH1 0x01
        # DUP1
        contract = Contract(bytecode="600180")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["1", "1"])

    def test_dup2(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='6001600081'_
        # PUSH1 0x01
        # PUSH1 0x00
        # DUP2
        contract = Contract(bytecode="6001600081")
        contract.execute(transaction={})
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
        contract.execute(transaction={})
        self.assertEqual(contract.stack,
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
        contract = Contract(bytecode="60016000600060006000600060006000600060006000600060006000600060008f")
        contract.execute(transaction={})
        self.assertEqual(contract.stack,
                         ["1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1"])

    def test_swap1(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='6002600190'_
        # PUSH1 0x02
        # PUSH1 0x01
        # SWAP1
        contract = Contract(bytecode="6002600190")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["1", "2"])

    def test_swap2(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='60026000600191'_
        # PUSH1 0x02
        # PUSH1 0x00
        # PUSH1 0x01
        # SWAP2
        contract = Contract(bytecode="60026000600191")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["1", "0", "2"])

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
        contract = Contract(bytecode="60026000600060006000600060006000600060006000600060006000600060019e")
        contract.execute(transaction={})
        self.assertEqual(contract.stack,
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
        contract = Contract(bytecode="600260006000600060006000600060006000600060006000600060006000600060019f")
        contract.execute(transaction={})
        self.assertEqual(contract.stack,
                         ["1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "2"])

    def test_codesize(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7cyyyyz5038'~zzz0z00y~~%01yz~_
        # PUSH29 0x0000000000000000000000000000000000000000000000000000000000
        # POP
        # CODESIZE
        contract = Contract(bytecode="7c00000000000000000000000000000000000000000000000000000000005038")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["20"])

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
        contract = Contract(bytecode="7dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f00000000000000000000000000000000000000000000000000000000000000005050602060006000396008601f600039")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, [])
        self.assertEqual("".join(contract.memory), "7f00000000000000ffffffffffffffffffffffffffffffffffffffffffffff7f")

    def test_gaslimit(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='45'_
        # GASLIMIT
        contract = Contract(bytecode="45")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["ffffffffffff"])

    def test_chainid(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='46'_
        # CHAINID
        contract = Contract(bytecode="46")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["1"])

    def test_basefee(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='48'_
        # BASEFEE
        contract = Contract(bytecode="48")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["a"])

    def test_pop(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='6201ec2150'_
        # PUSH3 0x01ec21
        # POP
        contract = Contract(bytecode="6201ec2150")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, [])

    def test_add(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600a600a017yyyyf600101'~zzzzzffy~~%01yz~_
        # PUSH1 0x0a
        # PUSH1 0x0a
        # ADD
        # PUSH32 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        # PUSH1 0x01
        # ADD
        contract = Contract(
            bytecode="600a600a017fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff600101")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["14", "0"])

    def test_mul(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600a600a027yyyyf600202'~zzzzzffy~~%01yz~_
        # PUSH1 0x0a
        # PUSH1 0x0a
        # MUL
        # PUSH32 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        # PUSH1 0x02
        # MUL
        contract = Contract(
            bytecode="600a600a027fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff600202")
        contract.execute(transaction={})
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
        contract.execute(transaction={})
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
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["1", "0"])

    def test_mod(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='6003600a066005601106'_
        # PUSH1 0x03
        # PUSH1 0x0a
        # MOD
        # PUSH1 0x05
        # PUSH1 0x11
        # MOD
        contract = Contract(bytecode="6003600a066005601106")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["1", "2"])

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
        contract = Contract(bytecode="6008600a600a08600260027fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff08")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["4", "1"])

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
        contract = Contract(bytecode="6008600a600a09600c7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff09")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["4", "9"])

    def test_lt(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='~a~910~a~a10'~600%01~_
        # PUSH1 0x0a
        # PUSH1 0x09
        # LT
        # PUSH1 0x0a
        # PUSH1 0x0a
        # LT
        contract = Contract(bytecode="600a600910600a600a10")
        contract.execute(transaction={})
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
        contract.execute(transaction={})
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
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["1", "0"])

    def test_iszero(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600a15600015'_
        # PUSH1 0x0a
        # ISZERO
        # PUSH1 0x00
        # ISZERO
        contract = Contract(bytecode="600a15600015")
        contract.execute(transaction={})
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
        contract.execute(transaction={})
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
        contract.execute(transaction={})
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
        contract.execute(transaction={})
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
        contract.execute(transaction={})
        self.assertEqual(
            contract.stack,
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
        contract = Contract(bytecode="60ff601f1a61ff00601e1a60ff60201a")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["ff", "ff", "0"])

    def test_shl(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='6z16z11b7fffyyyyyz6z41b'~zzzz00y~~%01yz~_
        # PUSH1 0x01
        # PUSH1 0x01
        # SHL
        # PUSH32 0xff00000000000000000000000000000000000000000000000000000000000000
        # PUSH1 0x04
        # SHL
        contract = Contract(bytecode="600160011b7fff0000000000000000000000000000000000000000000000000000000000000060041b")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["2", "f000000000000000000000000000000000000000000000000000000000000000"])

    def test_shr(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600260011c60ff60041c'_
        # PUSH1 0x02
        # PUSH1 0x01
        # SHR
        # PUSH1 0xff
        # PUSH1 0x04
        # SHR
        contract = Contract(bytecode="600260011c60ff60041c")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["1", "f"])

    def test_sload(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='602e600055600054600154'_
        # PUSH1 0x2e
        # PUSH1 0x00
        # SSTORE
        # PUSH1 0x00
        # SLOAD
        # PUSH1 0x01
        # SLOAD
        contract = Contract(bytecode="602e600055600054600154")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["2e", "0"])
        self.assertEqual(contract.storage, {"0": "2e"})

    def test_sstore(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='61ffff6000556100ff61230555'_
        # PUSH2 0xffff
        # PUSH1 0x00
        # SSTORE
        # PUSH2 0x00ff
        # PUSH2 0x2305
        # SSTORE
        contract = Contract(bytecode="61ffff6000556100ff61230555")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, [])
        self.assertEqual(contract.storage, {"0": "ffff", "2305": "ff"})

    def test_mstore(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='~052~152'~60ff600%01~_
        # PUSH1 0xff
        # PUSH1 0x00
        # MSTORE
        # PUSH1 0xff
        # PUSH1 0x01
        # MSTORE
        contract = Contract(bytecode="60ff60005260ff600152")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, [])
        self.assertEqual("".join(contract.memory), "0000000000000000000000000000000000000000000000000000000000000000ff00000000000000000000000000000000000000000000000000000000000000")

    def test_mstore8(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='61ffee60005360ff600153'_
        # PUSH2 0xffee
        # PUSH1 0x00
        # MSTORE8
        # PUSH1 0xff
        # PUSH1 0x01
        # MSTORE8
        contract = Contract(bytecode="61ffee60005360ff600153")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, [])
        self.assertEqual("".join(contract.memory), "eeff000000000000000000000000000000000000000000000000000000000000")

    def test_mload(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='7fyyyyyzff6z0526z0516z151'~zzzz00y~~%01yz~_
        # PUSH32 0x00000000000000000000000000000000000000000000000000000000000000ff
        # PUSH1 0x00
        # MSTORE
        # PUSH1 0x00
        # MLOAD
        # PUSH1 0x01
        # MLOAD
        contract = Contract(bytecode="7f00000000000000000000000000000000000000000000000000000000000000ff600052600051600151")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["ff", "ff00"])
        self.assertEqual("".join(contract.memory), "00000000000000000000000000000000000000000000000000000000000000ff0000000000000000000000000000000000000000000000000000000000000000")

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
        contract = Contract(bytecode="5960005150596039515059")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["0", "20", "60"])
        self.assertEqual("".join(contract.memory), "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")

    def test_jumpdest(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='5b5b'_
        # JUMPDEST
        # JUMPDEST
        contract = Contract(bytecode="5b5b")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, [])

    def test_jump(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='600456fe5b6001'_
        # PUSH1 0x04
        # JUMP
        # INVALID
        # JUMPDEST
        # PUSH1 0x01
        contract = Contract(bytecode="600456fe5b6001")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["1"])

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
        contract = Contract(bytecode="6000600a576001600c575bfe5b6001")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["1"])

    def test_pc(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&codeType=Bytecode&code='58585b58600158'_
        # PC
        # PC
        # JUMPDEST
        # PC
        # PUSH1 0x01
        # PC
        contract = Contract(bytecode="58585b58600158")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, ["0", "1", "3", "1", "6"])

    def test_callvalue(self):
        # https://www.evm.codes/playground?fork=shanghai&callValue=123456789&unit=Wei&codeType=Bytecode&code='34'_
        # CALLVALUE
        contract = Contract(bytecode="34")
        contract.execute(transaction={"value": "123456789"})
        self.assertEqual(contract.stack, ["75bcd15"])

    def test_calldataload(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&callData=0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff&codeType=Bytecode&code=%27600035601f35%27_
        # PUSH1 0x00
        # CALLDATALOAD
        # PUSH1 0x1f
        # CALLDATALOAD
        contract = Contract(bytecode="600035601f35")
        contract.execute(transaction={"data": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"})
        self.assertEqual(contract.stack, [
            "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            "ff00000000000000000000000000000000000000000000000000000000000000",
        ])

    def test_calldatasize(self):
        # https://www.evm.codes/playground?fork=shanghai&unit=Wei&callData=0xff&codeType=Bytecode&code=%2736%27_
        # CALLDATASIZE
        contract = Contract(bytecode="36")
        contract.execute(transaction={"data": "0xff"})
        self.assertEqual(contract.stack, ["1"])

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
        contract = Contract(bytecode="602060006000376008601f600037")
        contract.execute(transaction={"data": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"})
        self.assertEqual(contract.stack, [])
        self.assertEqual("".join(contract.memory), "ff00000000000000ffffffffffffffffffffffffffffffffffffffffffffffff")

    def test_log0(self):
        # PUSH1 0xff
        # PUSH1 0x00
        # MSTORE
        # PUSH1 0x20
        # PUSH1 0x00
        # LOG0
        contract = Contract(bytecode="60ff60005260206000a0")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, [])
        self.assertEqual(contract.logs, [{"data": "0xff"}])

    def test_log1(self):
        # PUSH1 0xff
        # PUSH1 0x00
        # MSTORE
        # PUSH32 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
        # PUSH1 0x20
        # PUSH1 0x00
        # LOG1
        contract = Contract(bytecode="60ff6000527fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef60206000a1")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, [])
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
        contract = Contract(bytecode="60ff6000527f000000000000000000000000bae7ebe87fc708426a193f49c4829cdc6221ac847fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef60206000a2")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, [])
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
        contract = Contract(bytecode="60ff6000527f0000000000000000000000004f6742badb049791cd9a37ea913f2bac38d012797f000000000000000000000000bae7ebe87fc708426a193f49c4829cdc6221ac847fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef60206000a3")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, [])
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
        # PUSH1 0x20
        # PUSH1 0x00
        # LOG4
        contract = Contract(bytecode="60ff6000526f000002ccc2087078963d621f42338ab07f0000000000000000000000004f6742badb049791cd9a37ea913f2bac38d012797f000000000000000000000000bae7ebe87fc708426a193f49c4829cdc6221ac847fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef60206000a4")
        contract.execute(transaction={})
        self.assertEqual(contract.stack, [])
        self.assertEqual(contract.logs, [{
            "data": "0xff",
            "topic0": "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
            "topic1": "0xbae7ebe87fc708426a193f49c4829cdc6221ac84",
            "topic2": "0x4f6742badb049791cd9a37ea913f2bac38d01279",
            "topic3": "0x2ccc2087078963d621f42338ab0",
        }])
