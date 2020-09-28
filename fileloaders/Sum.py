from collections import namedtuple
from typing import Optional, Tuple, List, Dict
from gspread import Worksheet as Sheet

from fileloaders.Enums import Enums
from fileloaders.Stocks import Operation, Commission
from fileloaders.common.Summarize import Summarize

SUM_SHEET_NAME: str = "_Summarization"
# Worksheets:
BROKER_STATISTIC_WORKSHEET_NAME: str = "Brokers statistic"


class BrokersStatistic(Summarize):
    # __sheet: Optional[Sheet] = None

    def __init__(self, operations: List[Operation], commissions: List[Commission], enums: Enums) -> None:
        super().__init__()
        self.operations: List[Operation] = operations
        self.commissions: List[Commission] = commissions
        self.enums: Enums = enums

        ColumnData = namedtuple('ColumnData', ['column_name', 'get_data_function', 'parameters'])
        column_order: List[ColumnData] = []
        column_order.append(ColumnData('Cash flow', self.__calculate_cash_flow, None))
        for commission in enums.get_commission_types():
             column_order.append(ColumnData(commission, self.__calculate_commission_by_type, commission))

        self.column_order: List[ColumnData] = column_order

    @classmethod
    def get_sheet_name(cls):
        return SUM_SHEET_NAME

    @classmethod
    def get_worksheet_name(cls):
        return BROKER_STATISTIC_WORKSHEET_NAME

    def refresh_data(self):
        # 1) get data
        Result = namedtuple('all_results', ['column_name', 'results'])
        all_results = []
        for item in self.column_order:
            # for currency in self.enums.get_currencies():
            #     result1 = item.get_data_function(item.parameters, currency=currency)
            all_results.append(Result(item.column_name, item.get_data_function(item.parameters)))

        return None
        # 2) write data
        data = []

        row_data = ['', '', '', 'Broker']
        data.append(row_data)

        row_data = ['', '', '']
        for broker in self.enums.get_brokers():
            row_data.append(broker)
        data.append(row_data)

        row_data = []

        self.clean_list()
        self.sheet.update('A1:Z100', data, raw=False)


    def __calculate_cash_flow(self, *args, **kwargs) -> dict:
        all_data = {}
        Key = namedtuple('key', ['broker', 'currency'])
        for operation in self.operations:
            key = Key(operation.get_broker(), operation.get_currency())
            if key not in all_data:
                all_data[key] = 0

            all_data[key] += operation.get_income_sum()
            all_data[key] += operation.get_expense_sum()

        return all_data

    def __calculate_commission_by_type(self, *args, **kwargs):
        all_data = {}
        Key = namedtuple('key', ['broker', 'currency'])
        for operation in self.operations:
            key = Key(operation.get_broker(), operation.get_currency())
            if key not in all_data:
                all_data[key] = 0

            all_data[key] += operation.get_income_sum()
            all_data[key] += operation.get_expense_sum()

        return all_data