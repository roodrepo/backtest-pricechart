import typing as t
from datafeed.other import YahooFinance
from datafeed.exchanges import Binance, FTX, CryptoDotCom


ExchangesType: t.Any[Binance, FTX, CryptoDotCom]
DatafeedType: t.Any[Binance, FTX, CryptoDotCom, YahooFinance]