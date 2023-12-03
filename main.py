from vm import EVM, TransactionMetadata

if __name__ == '__main__':
    evm = EVM()
    address_1 = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    evm.create_contract(bytecode="", address=address_1)
    operation = evm.execute_transaction(address=address_1, transaction_metadata=TransactionMetadata(), debug=True)
