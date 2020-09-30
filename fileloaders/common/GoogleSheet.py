from typing import Optional
from gspread import Worksheet as Sheet
from gspread.utils import a1_range_to_grid_range

from utilities.authorization import get_client


class GoogleSheet(object):
    def __init__(self) -> None:
        super().__init__()

    sheet: Optional[Sheet] = None

    @classmethod
    def get_sheet_name(cls):
        raise Exception("Not implemented")

    @classmethod
    def get_worksheet_name(cls):
        raise Exception("Not implemented")

    @classmethod
    def get_sheet(cls):
        if not cls.sheet:
            cls.sheet = get_client().open(cls.get_sheet_name()).worksheet(cls.get_worksheet_name())
        return cls.sheet

    @classmethod
    def get_all_values(cls):
        return cls.get_sheet().get_all_values()

    def _get_letter_by_number(self, number):
        all_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        return all_letters[number-1]

    def clean_list(self):
        self.get_sheet().clear()

        all_cells = "A1:" + str(self._get_letter_by_number(self.sheet.col_count)) + str(self.sheet.row_count)
        self.unmerge_cells(all_cells)

    def unmerge_cells(self, a1_range):
        grid_range = a1_range_to_grid_range(a1_range, self.sheet.id)

        body = {
            "requests": [
                {"unmergeCells": {"range": grid_range}}
            ]
        }

        self.sheet.spreadsheet.batch_update(body)
