import typing as t
import pandas_ta as ta
import pandas as pd
import numpy as np
from strategies._Strategy import _Strategy
from core.Signal import Signal

from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from scipy.signal import argrelextrema

class BollingerBand(_Strategy):
	
	enable_live: bool = False
	allow_long: bool = True
	allow_short: bool = True
	perc_min_profit: float = 0.03
	
	bbands_length: int = 20
	bbands_std: int = 2
	bbands_ddof: int = 0
	bbands_offset: int = 0
	order_aggreg: int = 10
	
	atr_length: int = 14
	sl_atr_factor: int = 2
	
	def init(self):
		
		self.bbands = self.I(
			self.bbandsOverride,
			close   = pd.Series(self.data.Close),
			length  = self.bbands_length,
			std     = self.bbands_std,
			ddof    = self.bbands_ddof,
			offset  = self.bbands_offset,
			overlay = True,
		)
		
		self.atr = self.I(
			ta.atr,
			high    = pd.Series(self.data.High),
			low     = pd.Series(self.data.Low),
			close   = pd.Series(self.data.Close),
			length  = self.atr_length,
			overlay = False,
		)
		
	def initLive(self, cash: int, commission: float, **kwargs) -> None:
		self.init()
		
		
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
		
		bbl = self.bbands[0]
		bbm = self.bbands[1]
		bbu = self.bbands[2]
		
		price = self.data.Close[-1]
		
		if (crossover(self.data.Close, bbm) or price < bbl[-1]):
			maxs = self.data.Close[argrelextrema(self.data.Close, np.greater_equal, order=self.order_aggreg)[0]]
			if len(maxs) >= 2:
				higher_highs    = True if maxs[-1] > maxs[-2] else False
				
				if higher_highs is True:
					self.triggerAction(
						self.buy,
						args_action= {
							'size' : 0.15,
							'sl'   : price - self.atr[-1] * self.sl_atr_factor,
						},
						args_signal = {
							'side'          : 'open',
							'position_side' : 'long',
						}
					)
					
		elif self.position.is_long is True:
			
			portion = None
			
			if crossover(self.data.Close, bbm):
				portion = 0.2
				
			elif price > bbu[-1]:
				portion = 0.3
			
			if portion is not None:
				self.triggerAction(
					self.position.close,
					args_action={
						'portion': portion,
					},
					args_signal={
						'side': 'close',
						'position_side': 'long',
					}
				)
			
		if price > bbu[-1]:
			mins = self.data.Close[argrelextrema(self.data.Close, np.less_equal, order=self.order_aggreg)[0]]

			if len(mins) >= 2:
				lower_lows      = True if  mins[-2] > mins[-1] else False
				
				if lower_lows is True:
					self.triggerAction(
						self.sell,
						args_action={
							'size' : 0.15,
							'sl'   : price + self.atr[-1] * self.sl_atr_factor,
						},
						args_signal={
							'side': 'open',
							'position_side': 'short',
						}
					)
			
		elif self.position.is_short is True:
			
			portion = None
			
			if crossover(bbm, self.data.Close):
				portion = 0.2
				
			elif price < bbl[-1]:
				portion = 0.3
			
			if portion is not None:
				self.triggerAction(
					self.position.close,
					args_action={
						'portion': portion,
					},
					args_signal={
						'side': 'close',
						'position_side': 'short',
					}
				)
				
	