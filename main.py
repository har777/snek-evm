from vm import Operation, OperationStatus

if __name__ == '__main__':
    operation = Operation(bytecode="")
    operation.transaction = {}
    operation.debug()
    while operation.status == OperationStatus.EXECUTING:
        operation.step()
        operation.debug()
