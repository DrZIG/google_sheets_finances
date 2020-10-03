from typing import List

from sheetloaders.Stocks import Operation, Commission
from utilities.general import loop_generator


def load_operations() -> List[Operation]:
    operations: List[Operation] = []
    pinned_rows_number: int = Operation.pinned_rows_number

    rows: List[List[str]] = Operation.get_all_values()
    for row in loop_generator(rows, pinned_rows_number + 1):
        operation = Operation()
        operation.load_properties(row)
        if not operation:
            break
        operations.append(operation)

    return operations


def load_commissions() -> List[Commission]:
    commissions: List[Commission] = []
    pinned_rows_number: int = Commission.pinned_rows_number

    rows: List[List[str]] = Commission.get_all_values()
    for row in loop_generator(rows, pinned_rows_number + 1):
        commission = Commission()
        commission.load_properties(row)
        if not commission:
            break
        commissions.append(commission)

    return commissions

# def load_enums():
#     pass
