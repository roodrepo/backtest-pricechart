import typing as t
from core.Timeframe import Timeframe
from core.Priceframe import Priceframe
import pandas_ta as ta
import pandas as pd
import numpy as np

from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from scipy.signal import argrelextrema

class BollingerBand(Strategy):
	
	enable_live: bool = False
	allow_long: bool = True
	allow_short: bool = True
	perc_min_profit: float = 0.03
	
	bbands_length: int = 20
	bbands_std: int = 2
	bbands_ddof: int = 0
	bbands_offset: int = 0
	order_aggreg: int = 4
	
	def init(self):
		
		self.bbands = self.I(
			self.bbandsOverride,
			pd.Series(self.data.Close),
			length  = self.bbands_length,
			std     = self.bbands_std,
			ddof    = self.bbands_ddof,
			offset  = self.bbands_offset,
			overlay = True,
		)
		
		# self.mins = self.I(
		# 	self.getExtremas,
		# 	pd.Series(self.data.Close),
		# 	peak_type       = 'min',
		# 	order_aggreg    = 4,
		# 	overlay         = True,
		# )
		#
		# self.maxs = self.I(
		# 	self.getExtremas,
		# 	self.data.Close,
		# 	peak_type       = 'max',
		# 	order_aggreg    = 4,
		# 	overlay         = True,
		# )
		
		# self.maxs = self.getExtremas(self.data.Close,
		# 	peak_type       = 'max',
		# 	order_aggreg    = 4,
		# )

		# print(self.maxs)
		
		
	def getExtremas(self, prices: pd.Series, peak_type: str, order_aggreg: int) -> pd.Series:
		if peak_type == 'min':
			return prices[argrelextrema(prices, np.less_equal, order=order_aggreg)[0]]
		
		elif peak_type == 'max':
			return argrelextrema(prices, np.greater_equal, order=order_aggreg)[0]
			# return prices[argrelextrema(prices, np.greater_equal, order=order_aggreg)[0]]
	
	# Removing the bands' width and percentage width to plot on same chart as price
	def bbandsOverride(self, *args, **kwargs):
		bbands = ta.bbands(*args, **kwargs)
		length = kwargs['length'] if 'length' in kwargs else args[1]
		std = str(float(kwargs['std'] if 'std' in kwargs else args[2]))

		bbands = bbands.drop(columns=[f'BBB_{length}_{std}', f'BBP_{length}_{std}'])
		return bbands
	
	def next(self):
		
		mins = self.data.Close[argrelextrema(self.data.Close, np.less_equal, order=self.order_aggreg)[0]]
		maxs = self.data.Close[argrelextrema(self.data.Close, np.greater_equal, order=self.order_aggreg)[0]]
		
		
		mins_mean = mins[-self.order_aggreg:].mean()
		
		print(mins_mean)
		
		bbl = self.bbands[0]
		bbm = self.bbands[1]
		bbu = self.bbands[2]
		
		if crossover(self.data.Close, bbm) or self.data.Close[-1] < bbl:
			self.buy(size= 0.15)
		
		elif self.data.Close[-1] > bbu:
			self.position.close(portion= 0.4)
	
	@classmethod
	def backtest(cls, priceframe: Priceframe, *, cash: int, commission: float, **kwargs) -> Backtest:
		return Backtest(priceframe.get(), cls, cash=cash, commission=commission, **kwargs)
	
	# def backtest(self, priceframe: Priceframe, pair: str, timeframe: Timeframe, exchange: ExchangesType):
	# 	pass
	#
	# def analyse(self, priceframe: Priceframe):
	#
	# 	bbands = ta.bbands(close= priceframe.get().close, length= 20, std= 2, ddof= 0, offset= 0)
	#
	#
	# def strategy(self, priceframe: Priceframe):
	# 	pass