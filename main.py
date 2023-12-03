from vm import Operation

if __name__ == '__main__':
    operation = Operation(bytecode="")
    operation.transaction = {}
    operation.debug()
    while not operation.stopped:
        operation.step()
        operation.debug()
