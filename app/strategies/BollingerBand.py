import pandas_ta as ta
import pandas as pd
import numpy as np
from strategies._Strategy import _Strategy

from backtesting.lib import crossover
from scipy.signal import argrelextrema

class BollingerBand(_Strategy):
	'''
	
	Indicators:
		- Bollinger Bands
		- ATR
		- Pivot levels
	
	Markets: spot, margin, futures
	Position sides: long, short
	
	Strategy long:
		Open:
			- Price crossing upward the bbm or price below bbl
			- Historical price must have higher highs
			
		Close:
			- Price crossing downward the bbm or price above bbu
			- Stop loss based on ATR
			
	Strategy short:
		Open:
			- Price crossing downward the bbm or price above bbu
			- Historical price must have lower lows
			
		Close:
			- Price crossing upward the bbm or price below bbl
			- Stop loss based on ATR
	
	'''
	
	enable_live     : bool  = True
	allow_long      : bool  = True
	allow_short     : bool  = True

	bbands_length   : int   = 20
	bbands_std      : int   = 2
	bbands_ddof     : int   = 0
	bbands_offset   : int   = 0
	order_aggreg    : int   = 10

	atr_length      : int   = 7
	sl_atr_factor   : int   = 3

	_acceptable_markets = {'spot', 'margin', 'futures'}
	
	def init(self):
		'''Function required by backtesting.py to init the indicators for the backtest'''
		
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
			plot    = False,
		)
		
	def initLive(self, **kwargs) -> None:
		'''Init strategy in live trading mode'''
		
		# self.data.Close = self.data.Close.to_numpy()
		self.init()
		
		
	def getExtremas(self, prices: pd.Series, peak_type: str, order_aggreg: int) -> pd.Series:
		'''Return all the previous pivot levels'''
		
		if peak_type == 'min':
			return prices[argrelextrema(prices, np.less_equal, order=order_aggreg)[0]]
		
		elif peak_type == 'max':
			return argrelextrema(prices, np.greater_equal, order=order_aggreg)[0]
	
	def bbandsOverride(self, *args, **kwargs):
		'''Removing the bands' width and percentage width to plot on same chart as price'''
		
		bbands  = ta.bbands(*args, **kwargs)
		length  = kwargs['length'] if 'length' in kwargs else args[1]
		std     = str(float(kwargs['std'] if 'std' in kwargs else args[2]))

		bbands = bbands.drop(columns=[f'BBB_{length}_{std}', f'BBP_{length}_{std}'])
		return bbands
	
	def next(self):
		'''Function required by backtesting.py for the backtest.'''
		
		close_price = self.data.Close
		
		if self.is_live is True:
			close_price = self.data.Close.to_numpy()
		
		
		bbl = self.bbands[0] # Bollinger band low
		bbm = self.bbands[1] # Bollinger band medium
		bbu = self.bbands[2] # Bollinger band up
		
		price = self.data.Close[-1]

		
		if self.allow_long is True:
			if (crossover(self.data.Close, bbm) or price < bbl[-1]):
				
				# Getting extrema take resources, we only calculate it when basic conditions are met
				maxs = self.data.Close[argrelextrema(close_price, np.greater_equal, order=self.order_aggreg)[0]]
				
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
			
			# Checking close condition only of at least one long position opened
			elif self.is_live or self.position.is_long is True:
				
				# Closing portion different according to the condition
				portion = None
				
				if crossover(self.data.Close, bbm):
					portion = 0.2
					
				elif price > bbu[-1]:
					portion = 0.3
				
				if portion is not None:
					self.triggerAction(
						self.position.close if self._broker is not None else None,
						args_action={
							'portion': portion,
						},
						args_signal={
							'side'          : 'close',
							'position_side' : 'long',
						}
					)
					
		if self.allow_short is True:
			if price > bbu[-1]:
				
				# Getting extrema take resources, we only calculate it when basic conditions are met
				mins = self.data.Close[argrelextrema(close_price, np.less_equal, order=self.order_aggreg)[0]]
	
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
								'side'          : 'open',
								'position_side' : 'short',
							}
						)
			
			# Checking close condition only of at least one short position opened
			elif self.is_live or self.position.is_short is True:
				
				# Closing portion different according to the condition
				portion = None
				
				if crossover(bbm, self.data.Close):
					portion = 0.2
					
				elif price < bbl[-1]:
					portion = 0.3
				
				if portion is not None:
					self.triggerAction(
						self.position.close if self._broker is not None else None,
						args_action={
							'portion': portion,
						},
						args_signal={
							'side'          : 'close',
							'position_side' : 'short',
						}
					)