# google_sheets_finances
Scripts for filling and updating predefined google sheets in which I keep track of finances and investment portfolios

**_Enums** sheet (3 first row):
|Currencies|RUB Tickers|USD Tickers|Instruments|Stock names|Types|Brokers|Commission types|Sectors|
|---|---|---|---|---|---|---|---|---|
|RUB|BANEP|AMZN|Shares. Reit|NYSE|ETF|IB|Tax|Communication Services|
|USD|CHMF|BA|Shares. IT|MCX|Bonds|VTB|Broker's comission|Real Estate|
|EUR|DSKY|BIIB|ETF|NASDAQ|Shares|Tinkoff|Service fee|Health Care|

**_Cash saving** sheet (example):
|Ticker|Currency|Broker|Price (Income)|Count (Income)|Income ↑|Date (Income)|Price (Expense)|Count (Expense)|Expense ↓|Date (Expense)| |Commission|Broker (Commission)|Currency (Commission)|Date (Commission)|Type|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|YNDX|RUB|Tinkoff|2 475,80|1|2 475,80|11.09.2019|2 480,00|1|2 480,00|18.11.2019| |99,00|Tinkoff|RUB|11.09.2019|Service fee|
|PYPL|USD|Tinkoff|104,04|5|520,20|01.10.2019| | | | | |7,43|Tinkoff|RUB|11.09.2019|Broker's comission|
|DAL|USD|IB|53,73|10|537,30|08.10.2019| | | | | |1,53|IB|USD|01.10.2019|Service fee|

As result executing of *_entrypoint.test_reload_broker_statistic_page* the following page will be refresh:
**_Summarization**:

| :                                         :|||:  Broker :|      |     |
|^^                                          |||: Tinkoff :| VTB  | IB  |
| :-------------- | :------------------ |:---- |:--------- |:---- |:--- |
| : Cash flow                         : | RUB  | 100000,87 | -    | -   |
| : Commissions : | Broker's comission  | RUB  | 100000,87 | -    | -   |
