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
	
	_nb_tickers = 600
	
	def __init__(self, nb_tickers: t.Optional[int] = None) -> None:
		if nb_tickers is not None:
			self.setNbTickers(nb_tickers)
	
	def setNbTickers(self, nb_tickers: int) -> None:
		self._nb_tickers = nb_tickers
	
	@classmethod
	def listPairs(cls) -> set:
		return cls._accepted_symbols
	
	def _toPriceframe(self, df: DataFrame) -> Priceframe:
		
		df.index.name = Priceframe.index_name
		
		return Priceframe(df)
	
	
	def priceframe(self, symbol: t.Union[str, set], timeframe: Timeframe, period: t.Optional[str] = None, date_from: t.Optional[datetime] = None, date_to: t.Optional[datetime] = None) -> Priceframe:
		'''
		
		:param symbol: Can accept multiple symbols at once
		:param timeframe: Timeframe used to get the tickers
		:param date_from: The default start time is defined by the numbers of tickers and ending date
		:param date_to: If not set, we return the price feed until current time
		:return: Formatted priceframe for the defined period
		'''
		if isinstance(symbol, str):
			_tmp = symbol.split(' ')
			symbol = set(_tmp)
		
		for _symbol in symbol:
			if _symbol not in self._accepted_symbols:
				raise Exception(f'The ticker {_symbol} is not accepted')
		
		symbol = " ".join(symbol)
		
		yf_extra_params = {}
		
		# If date_to is not set, we return the price feed until current time
		if date_to is None:
			date_to = datetime.utcnow()
		
		# otherwise, we add the end datetime in the parameters for yahoo finance
		else:
			yf_extra_params['end'] = date_to.strftime('%Y-%m-%d')
		
		# The default start time is defined by the numbers of tickers and ending date
		if date_from is None:
			date_from = date_to - timeframe.getInterval() * self._nb_tickers
			
		yf_extra_params['start'] = date_from.strftime('%Y-%m-%d')
		
		if 'end' not in yf_extra_params and period is not None:
			
			yf_extra_params['period'] = period
			del yf_extra_params['start']
		
		
		data = yf.download(
			tickers           = symbol,
			interval          = str(timeframe),
			auto_adjust       = True,
			prepost           = False,
			**yf_extra_params
		)
		
		
		return self._toPriceframe(data)