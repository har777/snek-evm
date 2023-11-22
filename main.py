from vm import Contract

if __name__ == '__main__':
    contract = Contract(bytecode="")
    contract.transaction = {}
    contract.debug()
    while not contract.stopped:
        contract.step()
        contract.debug()
