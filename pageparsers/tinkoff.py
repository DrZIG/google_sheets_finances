import json
from typing import Optional

from bs4 import BeautifulSoup
from pageparsers.page import Page


class Tinkoff(Page):
    def __init__(self, ref) -> None:
        super().__init__(ref)

    def parse_price(self) -> float:
        data = self._load_page()
        price = self.__get_price_data(data)
        if not price:
            raise Exception('Something wrong, call Dr.ZIG')
        return price

    def __get_price_data(self, text: str) -> Optional[float]:
        soup = BeautifulSoup(text, 'lxml')
        # soup = BeautifulSoup(text)
        # data = soup.find('div', {'data-qa-file': 'InvestChartPure'})  # .find('text').text
        # result = data.find('text', {'data-qa-file': 'Tooltip'})  # .text
        # result2 = soup.find_all('text')
        # print(result, "\n", result2)
        # div = soup.find('div', attrs={'data-qa-file': 'InvestChartPure'})
        # svg = div.find('svg', attrs={'data-qa-file': 'RightPanelPure'})
        # for child in svg.children():
        #     print(child)
        # try:
        #     result = json.loads(soup.text)
        # except Exception:
        #     pass

        # return result
        #


    # # loading files
    # page = 1
    # while True:
    #     data = load_user_data(user_id, page, s)
    #     if contain_movies_data(data):
    #         with open('./page_%d.html' % (page), 'w') as output_file:
    #             output_file.write(data.encode('cp1251'))
    #             page += 1
    #     else:
    #         break