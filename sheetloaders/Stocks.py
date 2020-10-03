import re
from typing import Optional
from gspread import Worksheet as Sheet

from sheetloaders.common.Row import Row
from sheetloaders.common.Worksheet import Worksheet

STOCKS_SHEET_NAME: str = "_Cash saving"
# Worksheets:
PLANS_WORKSHEET_NAME: str = "Plans"
OPERATIONS_WORKSHEET_NAME: str = "Operations"
DIVIDENDS_WORKSHEET_NAME: str = "Dividends"


class Operation(Worksheet, Row):
    attributes = {
        "Ticker": "ticker",
        "Currency": "currency",
        "Broker": "broker",
        "Price (Income)": "income_price",
        "Count (Income)": "income_count",
        "Income ↑": "income_sum",
        "Date (Income)": "income_date",
        "Price (Expense)": "expense_price",
        "Count (Expense)": "expense_count",
        "Expense ↓": "expense_sum",
        "Date (Expense)": "expense_date"
    }

    expected_missing_attributes = {
        "Commission": "commission_sum",
        "Broker (Commission)": "commission_broker",
        "Currency (Commission)": "commission_currency",
        "Date (Commission)": "commission_date",
        "Type": "commission_type"
    }

    # __sheet: Optional[Sheet] = None

    def __init__(self) -> None:
        super().__init__()

        self.ticker = None
        self.currency = None
        self.broker = None
        self.income_price = None
        self.income_count = None
        self.income_sum = None
        self.income_date = None
        self.expense_price = None
        self.expense_count = None
        self.expense_sum = None
        self.expense_date = None

    def __str__(self) -> str:
        return "{ticker} ({sum})".format(ticker=self.ticker, sum=self.income_sum)

    def __bool__(self):
        return bool(self.ticker)

    @classmethod
    def get_sheet_name(cls):
        return STOCKS_SHEET_NAME

    @classmethod
    def get_worksheet_name(cls):
        return OPERATIONS_WORKSHEET_NAME

    def get_currency(self):
        return self.currency

    def get_broker(self):
        return self.broker

    def get_expense_sum(self):
        pattern = re.compile(r'\s+')
        return float(re.sub(pattern, '', self.expense_sum.replace(",", ".")))

    def get_income_sum(self):
        pattern = re.compile(r'\s+')
        return float(re.sub(pattern, '', self.income_sum.replace(",", ".")))


class Commission(Worksheet, Row):
    attributes = {
        "Commission": "commission_sum",
        "Broker (Commission)": "commission_broker",
        "Currency (Commission)": "commission_currency",
        "Date (Commission)": "commission_date",
        "Type": "commission_type"
    }

    # __sheet: Optional[Sheet] = None
    expected_missing_attributes = Operation.attributes

    def __init__(self) -> None:
        super().__init__()

        self.commission_sum = None
        self.commission_broker = None
        self.commission_currency = None
        self.commission_date = None
        self.commission_type = None

    def __str__(self) -> str:
        return ""

    def __bool__(self):
        return bool(self.commission_sum)

    def get_type(self):
        return self.commission_type

    def get_currency(self):
        return self.commission_currency

    def get_broker(self):
        return self.commission_broker

    def get_sum(self):
        pattern = re.compile(r'\s+')
        return float(re.sub(pattern, '', self.commission_sum.replace(",", ".")))

    @classmethod
    def get_sheet_name(cls):
        return STOCKS_SHEET_NAME

    @classmethod
    def get_worksheet_name(cls):
        return OPERATIONS_WORKSHEET_NAME
