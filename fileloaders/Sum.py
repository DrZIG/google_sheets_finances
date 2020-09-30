from collections import namedtuple
from typing import List

from fileloaders.Enums import Enums
from fileloaders.Stocks import Operation, Commission
from fileloaders.common.Summarize import Summarize

SUM_SHEET_NAME: str = "_Summarization"
# Worksheets:
BROKER_STATISTIC_WORKSHEET_NAME: str = "Brokers statistic"


class BrokersStatistic(Summarize):

    def __init__(self, operations: List[Operation], commissions: List[Commission], enums: Enums) -> None:
        super().__init__()
        self.operations: List[Operation] = operations
        self.commissions: List[Commission] = commissions
        self.enums: Enums = enums

    @classmethod
    def get_sheet_name(cls) -> str:
        return SUM_SHEET_NAME

    @classmethod
    def get_worksheet_name(cls) -> str:
        return BROKER_STATISTIC_WORKSHEET_NAME

    def refresh_data(self) -> None:
        Key = namedtuple('key', ['broker', 'currency'])

        # 1) get data
        cash_flow = self.__calculate_cash_flow(self.operations)

        all_commissions = {}
        for commission in self.enums.get_commission_types():
            all_commissions[commission] = self.__calculate_commission_by_type(commission)

        summary = self.__calculate_summary(cash_flow, all_commissions)

        # 2) write data
        data = []

        row_data = ['', '', '', 'Broker']
        data.append(row_data)

        row_data = ['', '', '']
        for broker in self.enums.get_brokers():
            row_data.append(broker)
        data.append(row_data)

        for currency in self.enums.get_currencies():
            row_data = ['Cash flow', '', currency]
            for broker in self.enums.get_brokers():
                key = Key(broker, currency)
                row_data.append(round(cash_flow[key], 4) if key in cash_flow else "-")
            data.append(row_data)

        for commission in self.enums.get_commission_types():
            commission_data = all_commissions[commission] if commission in all_commissions else {}
            for currency in self.enums.get_currencies():
                row_data = ['Commissions', commission, currency]
                for broker in self.enums.get_brokers():
                    key = Key(broker, currency)
                    row_data.append(round(commission_data[key], 4) if key in commission_data else "-")
                data.append(row_data)

        for currency in self.enums.get_currencies():
            row_data = ['Summary', '', currency]
            for broker in self.enums.get_brokers():
                key = Key(broker, currency)
                if key in summary:
                    value = summary[key]
                    commission_sum = round(value["sum"], 4)
                    percent = round(value["percent"], 4)
                    row_data.append(f"{commission_sum} ({percent}%)")
                else:
                    row_data.append("-")
                # row_data.append(summary[key] if key in summary else 0)
            data.append(row_data)

        self.clean_list()
        self.sheet.update("A1:Z100", data, raw=False)

        # 3) make it beauty
        currencies_count = len(self.enums.get_currencies())

        # Broker
        self.sheet.merge_cells(f"D1:{self._get_letter_by_number(4 + len(self.enums.get_brokers()) - 1)}1")

        # Cash flow
        cash_flow_last_row = 3 + currencies_count - 1
        self.sheet.merge_cells(f"A3:B{cash_flow_last_row}")

        # Commissions
        commissions_last_row = cash_flow_last_row + len(self.enums.get_commission_types()) * currencies_count
        self.sheet.merge_cells(f"A{cash_flow_last_row + 1}:A{commissions_last_row}")
        last_row = cash_flow_last_row
        for _ in self.enums.get_commission_types():
            first_row = last_row + 1
            last_row = first_row + currencies_count - 1
            self.sheet.merge_cells(f"B{first_row}:B{last_row}")

        # Summary


    def __calculate_cash_flow(self, operations: List[Operation]) -> dict:
        Key = namedtuple('key', ['broker', 'currency'])
        all_data = {}
        for operation in operations:
            key = Key(operation.get_broker(), operation.get_currency())
            if key not in all_data:
                all_data[key] = 0

            all_data[key] += operation.get_income_sum()
            all_data[key] += operation.get_expense_sum()

        return all_data

    def __calculate_commission_by_type(self, commission_type) -> dict:
        Key = namedtuple('key', ['broker', 'currency'])
        all_data = {}
        for commission in [commission for commission in self.commissions if commission.get_type() == commission_type]:
            key = Key(commission.get_broker(), commission.get_currency())
            if key not in all_data:
                all_data[key] = 0

            all_data[key] += commission.get_sum()

        return all_data

    def __calculate_summary(self, cash_flow: dict, all_commissions: dict) -> dict:
        all_data = {}
        for key, cash in cash_flow.items():
            commission_sum = 0
            for _, commission_data in all_commissions.items():
                if key in commission_data:
                    commission_sum += commission_data[key]

            percent = commission_sum * 100 / cash
            all_data[key] = {"sum": commission_sum, "percent": percent}

        return all_data
