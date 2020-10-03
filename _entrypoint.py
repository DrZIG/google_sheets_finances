import unittest
from typing import List

from sheetloaders.Enums import Enums
from sheetloaders.Stocks import Operation, Commission
from sheetloaders.Sum import BrokersStatistic
from utilities.authorization import close_session
from utilities.class_loader import load_operations, load_commissions


class EntryPoint(unittest.TestCase):

    def test_update_tikers_information(self) -> None:
        """

        :return:
        """

    def test_reload_broker_statistic_page(self):
        """
        			                Commissions							
	            Cash flow       	service fee		brocker comissions		ndfl		Summary	
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

        close_session()
