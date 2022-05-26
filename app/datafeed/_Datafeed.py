import inspect
import typing as t
from datetime import datetime

from core.Priceframe import Priceframe
from core.Timeframe import Timeframe
from core.ErrorMessages import ERROR_MESSAGES

class _Datafeed:
	'''Abstract parent class for all datafeed platforms'''
	
	@classmethod
	def connect(cls) -> None:
		'''Throw exception if not implemented in the children'''
		raise(ERROR_MESSAGES['missing_method'] % (inspect.currentframe().f_code.co_name, cls.__name__))
	
	@classmethod
	def listPairs(cls) -> set:
		'''Throw exception if not implemented in the children'''
		raise(ERROR_MESSAGES['missing_method'] % (inspect.currentframe().f_code.co_name, cls.__name__))
	
	@classmethod
	def priceframe(cls, symbol: str, timeframe: Timeframe, date_from: t.Optional[datetime] = None, date_to: t.Optional[datetime] = None) -> Priceframe:
		'''Throw exception if not implemented in the children'''
		raise(ERROR_MESSAGES['missing_method'] % (inspect.currentframe().f_code.co_name, cls.__name__))