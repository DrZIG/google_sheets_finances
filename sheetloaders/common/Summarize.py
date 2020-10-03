from sheetloaders.common.GoogleSheet import GoogleSheet
from utilities.authorization import get_client


class Summarize(GoogleSheet):
    def __init__(self) -> None:
        super().__init__()

    def refresh_data(self, **kwargs):
        raise Exception("Not implemented")
