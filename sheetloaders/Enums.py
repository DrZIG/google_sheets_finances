from typing import Optional, List
from gspread import Worksheet as Sheet
from sheetloaders.common.GoogleSheet import GoogleSheet
from sheetloaders.common.Row import Row
from sheetloaders.common.Worksheet import Worksheet
from utilities.general import loop_generator

ENUMS_SHEET_NAME: str = "_Enums"
# Worksheets:
ENUMS_WORKSHEET_NAME = "Enums"
TICKERS_WORKSHEET_NAME = "Tickers"
CONSTANTS_WORKSHEET_NAME = "Constants"


class Ticker(GoogleSheet):
    attributes = {
        "Company": "name",
        "Ticker": "ticker",
        "Currency": "currency",
        "Instrument type": "instrument_type",
        "Stock name": "stock",
        "Current price": "price",
        "Ref to price page": "ref",
        "Описание": None
    }
    __sheet: Optional[Sheet] = None

    def __init__(self) -> None:
        super().__init__()

        self.name = None
        self.ticker = None
        self.currency = None
        self.instrument_type = None
        self.stock = None
        self.price = None
        self.ref = None

    def __setattr__(self, key, value):
        if value == '#N/A':
            return
        else:
            super.__setattr__(self, key, value)

    def __str__(self) -> str:
        return self.name

class Enums(Worksheet):
    class __Enums(Row):
        attributes: dict = {
            "Currencies": "currencies",
            "RUB Tickers": "rub_tickers",  # deprecated
            "USD Tickers": "usd_tickers",  # deprecated
            "Instruments": "instruments",
            "Stock names": "stock_names",
            "Types": "types",
            "Brokers": "brokers",
            "Commission types": "commission_types",
            "Sectors": "sectors"
        }

        __sheet: Optional[Sheet] = None

        def __init__(self):
            super().__init__()
            self.__load_enums()

        def __load_enums(self):
            pinned_rows_number: int = Enums.pinned_rows_number

            rows: List[List[str]] = self.get_all_values()
            for attribute_key, attribute_value in self.attributes.items():
                column = self.properties_order.index(attribute_key)
                for row in loop_generator(rows, pinned_rows_number + 1):
                    value = row[column]
                    if not value:
                        break
                    if not hasattr(self, attribute_value):
                        self.__setattr__(attribute_value, [])
                    self.__getattribute__(attribute_value).append(value)

            self._enums_loaded = True

        def __setattr__(self, key, value):
            if value == '#N/A':
                return
            else:
                super.__setattr__(self, key, value)

        # def __getitem__(self, item):
        #     return self

        # def __getattr__(self, item):
        #     pass

        @classmethod
        def get_sheet_name(cls):
            return Enums.get_sheet_name()

        @classmethod
        def get_worksheet_name(cls):
            return Enums.get_worksheet_name()

        def __bool__(self):
            return self._enums_loaded

    instance: __Enums = None
    # _enums_loaded: bool = False
    # currencies: list = []
    # rub_tickers: list = []
    # usd_tickers: list = []
    # instruments: list = []
    # stock_names: list = []
    # types: list = []
    # brokers: list = []
    # commission_types: list = []

    def __init__(self) -> None:
        super().__init__()
        if not Enums.instance:
            Enums.instance = Enums.__Enums()

    def __setattr__(self, key, value):
        if value == '#N/A':
            return
        else:
            super.__setattr__(self, key, value)

    def __getitem__(self, item):
        pass


    @classmethod
    def get_brokers(cls) -> list:
        cls.__check_enums()
        return cls.instance.__getattribute__("brokers")

    @classmethod
    def get_commission_types(cls) -> List[str]:
        cls.__check_enums()
        return cls.instance.__getattribute__("commission_types")

    @classmethod
    def get_currencies(cls) -> List[str]:
        cls.__check_enums()
        return cls.instance.__getattribute__("currencies")

    @classmethod
    def get_sheet_name(cls):
        return ENUMS_SHEET_NAME

    @classmethod
    def get_worksheet_name(cls):
        return ENUMS_WORKSHEET_NAME

    @classmethod
    def __check_enums(cls):
        if not cls.instance:
            cls.instance = Enums.__Enums()