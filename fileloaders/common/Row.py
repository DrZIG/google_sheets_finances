from fileloaders.common.GoogleSheet import GoogleSheet
from utilities.authorization import get_client


def _load_properties_order(spreadsheet_name: str, worksheet_name: str) -> list:
    sheet = get_client().open(spreadsheet_name).worksheet(worksheet_name)
    return sheet.row_values(1)


class Row(GoogleSheet):
    properties_order: list = []
    attributes = {}
    expected_missing_attributes = {}

    def __init__(self) -> None:
        super().__init__()

        if not self.get_properties_order():
            self._set_properties_order(_load_properties_order(self.get_sheet_name(), self.get_worksheet_name()))
            self._check_attribute_existing()

    def __setattr__(self, key, value):
        if value == '#N/A':
            return
        else:
            super.__setattr__(self, key, value)

    def __bool__(self):
        raise Exception("Not implemented")

    @classmethod
    def get_properties_order(cls) -> list:
        return cls.properties_order

    @classmethod
    def _set_properties_order(cls, properties_order: list) -> None:
        cls.properties_order = properties_order

    @classmethod
    def _check_attribute_existing(cls) -> None:
        missing_list: list = []
        for prop in cls.properties_order:
            if prop and prop not in cls.attributes:
                if prop in cls.expected_missing_attributes:
                    continue
                missing_list.append(prop)
        if missing_list:
            raise Exception('{object_name} has missing attributes: {missing_list}'.format(
                object_name=cls.__class__.__name__, missing_list=missing_list))

    def load_properties(self, properties: list) -> None:
        for column_number, prop in enumerate(self.get_properties_order()):
            if not prop or prop not in self.attributes:
                continue
            if self.attributes[prop] and column_number < len(properties):
                self.__setattr__(self.attributes[prop], properties.__getitem__(column_number))
