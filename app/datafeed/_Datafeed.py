import inspect
import typing as t
from datetime import datetime

from core.Priceframe import Priceframe
from core.Timeframe import Timeframe

ERROR_MESSAGES: dict = {

}

class _Datafeed:
	
	@classmethod
	def connect(cls) -> None:
		raise(f'The method "{inspect.currentframe().f_code.co_name}" is not implemented in class {cls.__name__}')
	
	@classmethod
	def listPairs(cls) -> set:
		raise(f'The method "{inspect.currentframe().f_code.co_name}" is not implemented in class {cls.__name__}')
	
	@classmethod
	def priceframe(cls, symbol: str, timeframe: Timeframe, date_from: t.Optional[datetime] = None, date_to: t.Optional[datetime] = None) -> Priceframe:
		raise(f'The method "{inspect.currentframe().f_code.co_name}" is not implemented in class {cls.__name__}')