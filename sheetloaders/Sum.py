from collections import namedtuple
from typing import List

from general.Enums import HorizontalAlignment, VerticalAlignment, WrapStrategy
from sheetloaders.Enums import Enums
from sheetloaders.Stocks import Operation, Commission
from sheetloaders.common.Summarize import Summarize

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
        all_merge_ranges = []
        horizontal_alignment_ranges = []
        vertical_alignment_ranges = []
        wrap_strategy_ranges = []

        # Broker
        broker_range = f"D1:{self._get_letter_by_number(4 + len(self.enums.get_brokers()) - 1)}1"
        all_merge_ranges.append(broker_range)
        horizontal_alignment_ranges.append(broker_range)

        # Cash flow
        cash_flow_last_row = 3 + currencies_count - 1
        cash_flow_range = f"A3:B{cash_flow_last_row}"
        all_merge_ranges.append(cash_flow_range)
        # horizontal_alignment_ranges.append(cash_flow_range)
        vertical_alignment_ranges.append(cash_flow_range)

        # Commissions
        commissions_last_row = cash_flow_last_row + len(self.enums.get_commission_types()) * currencies_count
        commissions_range = f"A{cash_flow_last_row + 1}:A{commissions_last_row}"
        all_merge_ranges.append(commissions_range)
        vertical_alignment_ranges.append(commissions_range)
        last_row = cash_flow_last_row
        for _ in self.enums.get_commission_types():
            first_row = last_row + 1
            last_row = first_row + currencies_count - 1
            commission_range = f"B{first_row}:B{last_row}"
            all_merge_ranges.append(commission_range)
            vertical_alignment_ranges.append(commission_range)
            wrap_strategy_ranges.append(commission_range)

        # Summary
        last_summary_row = last_row + currencies_count
        summary_range = f"A{last_row + 1}:B{last_summary_row}"
        all_merge_ranges.append(summary_range)
        # horizontal_alignment_ranges.append(summary_range)
        vertical_alignment_ranges.append(summary_range)

        self.merge_cells(all_merge_ranges)

        # alignment
        self.set_horizontal_alignment(horizontal_alignment_ranges, HorizontalAlignment.CENTER)
        self.set_vertical_alignment(vertical_alignment_ranges, VerticalAlignment.CENTER)

        # PositionedLayout. Tests shows that PositionedLayout need to be corrected only for commission types
        self.set_wrap_strategy(wrap_strategy_ranges, WrapStrategy.WRAP)


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
