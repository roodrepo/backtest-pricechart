import typing as t
from datetime import timedelta

class Timeframe:
	'''Limit and format acceptable timeframes'''
	
	_accepted_timeframes: set = {
		'1m',
		'5m',
		'15m',
		'30m',
		'1h',
		'2h',
		'4h',
		'6h',
		'8h',
		'12h',
		'1d',
		'3d',
		'5d',
		'1w',
		'1M',
	}
	
	current_timeframe: str
	
	def __init__(self, timeframe: str) -> None:
		self.set(timeframe)
		
	def __str__(self):
		return self.get()
	
	def _checkTF(self, timeframe: str) -> None:
		if timeframe is None or timeframe not in self._accepted_timeframes:
			raise Exception(f'{timeframe} is not acceptable')
	
	def set(self, timeframe: str):
		self._checkTF(timeframe)
		
		self.current_timeframe = timeframe
		
	def get(self):
		return self.current_timeframe
	
	def getInterval(self, timeframe: t.Optional[str] = None) -> timedelta:
		'''Get interval of timeframe'''
		
		
		tf = timeframe
		if tf is None:
			tf = self.current_timeframe

		self._checkTF(tf)

		_period = int(tf[:-1])
		_time_length = tf[-1]
		
		delta_params = {}
		
		if _time_length == 'm':
			delta_params['minutes'] = _period

		elif _time_length ==  'h':
			delta_params['hours'] = _period

		elif _time_length ==  'd':
			delta_params['days'] = _period

		elif _time_length ==  'w':
			delta_params['weeks'] = _period

		elif _time_length ==  'M':
			# Be more accurate using relativedelta
			delta_params['days'] = _period * 30
			
		return timedelta(**delta_params)

		
		
		
		
		
	