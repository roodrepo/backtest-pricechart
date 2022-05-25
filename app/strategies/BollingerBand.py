import typing as t
from core.Timeframe import Timeframe
from core.Priceframe import Priceframe
from core.Types import ExchangesType

class BollingerBand:
	
	_long: bool = True
	_short: bool = True
	
	_parameters: dict = {
	}
	
	def backtest(self, priceframe: Priceframe, pair: str, timeframe: Timeframe, exchange: ExchangesType):
		pass
	
	def analyse(self):
		pass
	
	def strategy(self, priceframe: Priceframe):
		pass