# snek-evm

An in-progress implementation of the EVM in python.

## Progress

| Code | Name           | Implemented |
|------|----------------|-------------|
| 00   | STOP           | ✅           |
| 01   | ADD            | ✅           |
| 02   | MUL            | ✅           |
| 03   | SUB            | ✅           |
| 04   | DIV            | ✅           |
| 05   | SDIV           |             |
| 06   | MOD            | ✅           |
| 07   | SMOD           |             |
| 08   | ADDMOD         | ✅           |
| 09   | MULMOD         | ✅           |
| 0A   | EXP            |             |
| 0B   | SIGNEXTEND     |             |
| 10   | LT             | ✅           |
| 11   | GT             | ✅           |
| 12   | SLT            |             |
| 13   | SGT            |             |
| 14   | EQ             | ✅           |
| 15   | ISZERO         | ✅           |
| 16   | AND            | ✅           |
| 17   | OR             | ✅           |
| 18   | XOR            | ✅           |
| 19   | NOT            | ✅           |
| 1A   | BYTE           | ✅           |
| 1B   | SHL            | ✅           |
| 1C   | SHR            | ✅           |
| 1D   | SAR            |             |
| 20   | SHA3           | ✅           |
| 30   | ADDRESS        |             |
| 31   | BALANCE        |             |
| 32   | ORIGIN         |             |
| 33   | CALLER         |             |
| 34   | CALLVALUE      | ✅           |
| 35   | CALLDATALOAD   | ✅           |
| 36   | CALLDATASIZE   | ✅           |
| 37   | CALLDATACOPY   | ✅           |
| 38   | CODESIZE       | ✅           |
| 39   | CODECOPY       | ✅           |
| 3A   | GASPRICE       |             |
| 3B   | EXTCODESIZE    |             |
| 3C   | EXTCODECOPY    |             |
| 3D   | RETURNDATASIZE |             |
| 3E   | RETURNDATACOPY |             |
| 3F   | EXTCODEHASH    |             |
| 40   | BLOCKHASH      |             |
| 41   | COINBASE       |             |
| 42   | TIMESTAMP      |             |
| 43   | NUMBER         |             |
| 44   | PREVRANDAO     |             |
| 45   | GASLIMIT       | ✅           |
| 46   | CHAINID        | ✅           |
| 47   | SELFBALANCE    |             |
| 48   | BASEFEE        | ✅           |
| 50   | POP            | ✅           |
| 51   | MLOAD          | ✅           |
| 52   | MSTORE         | ✅           |
| 53   | MSTORE8        | ✅           |
| 54   | SLOAD          | ✅           |
| 55   | SSTORE         | ✅           |
| 56   | JUMP           | ✅           |
| 57   | JUMPI          | ✅           |
| 58   | PC             | ✅           |
| 59   | MSIZE          | ✅           |
| 5A   | GAS            |             |
| 5B   | JUMPDEST       | ✅           |
| 5F   | PUSH0          | ✅           |
| 60   | PUSH1          | ✅           |
| 61   | PUSH2          | ✅           |
| 62   | PUSH3          | ✅           |
| 63   | PUSH4          | ✅           |
| 64   | PUSH5          | ✅           |
| 65   | PUSH6          | ✅           |
| 66   | PUSH7          | ✅           |
| 67   | PUSH8          | ✅           |
| 68   | PUSH9          | ✅           |
| 69   | PUSH10         | ✅           |
| 6A   | PUSH11         | ✅           |
| 6B   | PUSH12         | ✅           |
| 6C   | PUSH13         | ✅           |
| 6D   | PUSH14         | ✅           |
| 6E   | PUSH15         | ✅           |
| 6F   | PUSH16         | ✅           |
| 70   | PUSH17         | ✅           |
| 71   | PUSH18         | ✅           |
| 72   | PUSH19         | ✅           |
| 73   | PUSH20         | ✅           |
| 74   | PUSH21         | ✅           |
| 75   | PUSH22         | ✅           |
| 76   | PUSH23         | ✅           |
| 77   | PUSH24         | ✅           |
| 78   | PUSH25         | ✅           |
| 79   | PUSH26         | ✅           |
| 7A   | PUSH27         | ✅           |
| 7B   | PUSH28         | ✅           |
| 7C   | PUSH29         | ✅           |
| 7D   | PUSH30         | ✅           |
| 7E   | PUSH31         | ✅           |
| 7F   | PUSH32         | ✅           |
| 80   | DUP1           | ✅           |
| 81   | DUP2           | ✅           |
| 82   | DUP3           | ✅           |
| 83   | DUP4           | ✅           |
| 84   | DUP5           | ✅           |
| 85   | DUP6           | ✅           |
| 86   | DUP7           | ✅           |
| 87   | DUP8           | ✅           |
| 88   | DUP9           | ✅           |
| 89   | DUP10          | ✅           |
| 8A   | DUP11          | ✅           |
| 8B   | DUP12          | ✅           |
| 8C   | DUP13          | ✅           |
| 8D   | DUP14          | ✅           |
| 8E   | DUP15          | ✅           |
| 8F   | DUP16          | ✅           |
| 90   | SWAP1          | ✅           |
| 91   | SWAP2          | ✅           |
| 92   | SWAP3          | ✅           |
| 93   | SWAP4          | ✅           |
| 94   | SWAP5          | ✅           |
| 95   | SWAP6          | ✅           |
| 96   | SWAP7          | ✅           |
| 97   | SWAP8          | ✅           |
| 98   | SWAP9          | ✅           |
| 99   | SWAP10         | ✅           |
| 9A   | SWAP11         | ✅           |
| 9B   | SWAP12         | ✅           |
| 9C   | SWAP13         | ✅           |
| 9D   | SWAP14         | ✅           |
| 9E   | SWAP15         | ✅           |
| 9F   | SWAP16         | ✅           |
| A0   | LOG0           | ✅           |
| A1   | LOG1           | ✅           |
| A2   | LOG2           | ✅           |
| A3   | LOG3           | ✅           |
| A4   | LOG4           | ✅           |
| F0   | CREATE         |             |
| F1   | CALL           | ✅           |
| F2   | CALLCODE       |             |
| F3   | RETURN         | ✅           |
| F4   | DELEGATECALL   |             |
| F5   | CREATE2        |             |
| FA   | STATICCALL     |             |
| FD   | REVERT         | ✅           |
| FE   | INVALID        | ✅           |
| FF   | SELFDESTRUCT   |             |
