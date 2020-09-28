from utilities.authorization import get_session


class Page(object):
    def __init__(self, ref) -> None:
        super().__init__()
        self.ref = ref

    def parse_price(self):
        pass

    def _load_page(self):
        request = get_session().get(self.ref)
        # return request.text
        return request.content

def page_fabric(reference: str) -> Page:
    from pageparsers.tinkoff import Tinkoff

    if reference.startswith("https://www.tinkoff.ru/"):
        return Tinkoff(reference)

    return Page(reference)

def test():
    import requests
    from bs4 import BeautifulSoup as bs
    import re
    import locale

    res = requests.get(
        'http://abacus.realendpoints.com/ConsoleTemplate.aspx?act=qlrd&req=nav&mop=abacus!main&pk=ed5a81ad-9367-41c8-aa6b-18a08199ddcf&ab-eff=1000&ab-tox=0.1&ab-nov=1&ab-rare=1&ab-pop=1&ab-dev=1&ab-prog=1.0&ab-need=1&ab-time=1543102810')
    soup = bs(res.content, 'lxml')
    script = soup.select('script')[19]
    items = str(script).split('series:')
    item = items[2].split('exporting')[0][:-15]
    p1 = re.compile('name:(.*)]')
    p2 = re.compile('(\d+\.\d+)+')
    it = re.finditer(p1, item)
    names = [match.group(1).split(',')[0].strip().replace("'", '') for match in it]
    it2 = re.finditer(p2, item)
    allNumbers = [float(match.group(1)) for match in it2]
    actualAnnuals = allNumbers[0::2]
    abacusAnnuals = allNumbers[1::2]
    actuals = list(zip(names, actualAnnuals))
    abacus = list(zip(names, abacusAnnuals))

    # Examples:
    print(actuals, abacus)

    locale.setlocale(locale.LC_ALL, 'English')
    print(locale.format('%.2f', sum(actualAnnuals), True))