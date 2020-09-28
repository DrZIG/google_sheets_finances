import unittest
from typing import List

from fileloaders.Enums import Enums
from fileloaders.Stocks import Operation, Commission
from fileloaders.Sum import BrokersStatistic
from utilities.authorization import close_session
from utilities.class_loader import load_operations, load_commissions
from utilities.general import clean_worksheet


class EntryPoint(unittest.TestCase):

    def test_reload_broker_statistic_page(self):
        """
        На странице должна быть инфа по брокерам:
        1) Общая сумма движений денежных средств в рублях/долларах/всего
        2) обшая сумма уплоченных комиссий по типам и валютам и всего
        3) комиссии в процентах тоже как-то должны отражаться
        4) Если добавится новый брокер, всё должно автоматом перечситываться
        """

        """
        			                Commissions							
	            Движения средств	service fee		brocker comissions		ndfl		Всего	
        Broker	Rub	usd	            rub	usd	        rub	usd	                rub	usd	    rub	        usd
        tinkoff	1000 100            50 5	        200	20	                5	0	    500 (10%)	100 (10%)
        vtb 	2000  200           0 0             200	20	                0	0	    300 (13%)	50 (15%)
        """

        # temporarry commented
        operations: List[Operation] = load_operations()
        commissions: List[Commission] = load_commissions()
        enums: Enums = Enums()
        broker_statistics: BrokersStatistic = BrokersStatistic(operations, commissions, enums)
        broker_statistics.refresh_data()

        # all currencies

        # all brokers

        # all commission types

        close_session()
        # summarization_sheet = get_client().open(SUM_SHEET_NAME)
         # = sheet.worksheet("Brokers statistic")




