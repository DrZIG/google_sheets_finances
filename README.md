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

<table>
  <tr>
    <td></td><td></td><td></td><td colspan="3">Broker</td>
   </tr>
  <tr>
    <td></td><td></td><td></td><td>Tinkoff</td><td>VTB</td><td>IB</td>
  </tr>
  <tr>
    <td rowspan="3" colspan="2">Cash flow</td><td>RUB</td><td>100500</td><td>-</td><td>-</td>
  </tr>
  <tr>
    <td>USD</td><td>1050</td><td>350</td><td>-</td>
  </tr>
  <tr>
    <td>EUR</td><td>675</td><td>-</td><td>-</td>
  </tr>
  <tr>
    <td rowspan="6">Commissions</td><td rowspan="3">Broker's comission</td><td>RUB</td><td>950</td><td>150</td><td>-</td>
  </tr>
  <tr>
    <td>USD</td><td>9,87</td><td>1,6</td><td>-</td>
  </tr>
  <tr>
    <td>EUR</td><td>-</td><td>-</td><td>-</td>
  </tr>
  <tr>
    <td rowspan="3">Service fee</td><td>RUB</td><td>390</td><td>-</td><td>-</td>
  </tr>
  <tr>
    <td>USD</td><td>3,19</td><td>-</td><td>-</td>
  </tr>
  <tr>
    <td>EUR</td><td>-</td><td>-</td><td>-</td>
  </tr>
  <tr>
    <td rowspan="3" colspan="2">Summary</td><td>RUB</td><td>1400 (0,345%)</td><td>-</td><td>-</td>
  </tr>
  <tr>
    <td>USD</td><td>13 (0,26%)</td><td>1,46 (0,035%)</td><td>-</td>
  </tr>
  <tr>
    <td>EUR</td><td>-</td><td>-</td><td>-</td>
  </tr>
</table>
