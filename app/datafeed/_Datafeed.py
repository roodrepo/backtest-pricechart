import inspect
import typing as t
from datetime import datetime

from core.Priceframe import Priceframe
from core.Timeframe import Timeframe

ERROR_MESSAGES: dict = {
	'missing_method': 'The method "%s" is not implemented in class %s'
}

class _Datafeed:
	
	@classmethod
	def connect(cls) -> None:
		raise(ERROR_MESSAGES['missing_method'] % (inspect.currentframe().f_code.co_name, cls.__name__))
	
	@classmethod
	def listPairs(cls) -> set:
		raise(ERROR_MESSAGES['missing_method'] % (inspect.currentframe().f_code.co_name, cls.__name__))
	
	@classmethod
	def priceframe(cls, symbol: str, timeframe: Timeframe, date_from: t.Optional[datetime] = None, date_to: t.Optional[datetime] = None) -> Priceframe:
		raise(ERROR_MESSAGES['missing_method'] % (inspect.currentframe().f_code.co_name, cls.__name__))