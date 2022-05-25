import typing as t
from datetime import datetime
from pandas import DataFrame
import yfinance as yf

from datafeed._Datafeed import _Datafeed
from core.Priceframe import Priceframe
from core.Timeframe import Timeframe

class YahooFinance(_Datafeed):
	
	_accepted_symbols: set = {
		'AAPL',
		'AMZN',
		'GOOGL',
	}
	_mapping_timeframe_platform: set = {
		'1m'  : '1m',
		'2m'  : '2m',
		'5m'  : '5m',
		'15m' : '15m',
		'30m' : '30m',
		'90m' : '90m',
		'1h'  : '1h',
		'1d'  : '1d',
		'5d'  : '5d',
		'1w'  : '1wk',
		'1M'  : '1mo',
		'3M'  : '3mo',
	}
	
	_nb_tickers = 300
	
	def __init__(self, nb_tickers: t.Optional[int] = None) -> None:
		if nb_tickers is not None:
			self.setNbTickers(nb_tickers)
	
	def setNbTickers(self, nb_tickers: int) -> None:
		self._nb_tickers = nb_tickers
	
	@classmethod
	def listPairs(cls) -> set:
		return cls._accepted_symbols
	
	def _toPriceframe(self, df: DataFrame) -> Priceframe:
		
		df.rename(columns={"Datetime": "time", "Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"})
		
		return Priceframe(df)
	
	
	def priceframe(self, symbol: str, timeframe: Timeframe, date_from: t.Optional[datetime] = None, date_to: t.Optional[datetime] = None) -> Priceframe:
		
		if symbol not in self._accepted_symbols:
			raise Exception(f'The ticker {symbol} is not accepted')
		
		if date_from is None:
			date_from = datetime.now() - timeframe.getInterval() * self._nb_tickers
			
		data = yf.download(
			tickers= symbol,
			# period = '1mo',
			start = date_from.strftime('%Y-%m-%d'),
			interval = str(timeframe),
			auto_adjust = True
		)
		
		return self._toPriceframe(data)