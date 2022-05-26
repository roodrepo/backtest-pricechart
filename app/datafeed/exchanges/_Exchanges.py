from datafeed._Datafeed import _Datafeed
import inspect
import typing as t
from core.ErrorMessages import ERROR_MESSAGES
from core.Signal import Signal

class _Exchanges(_Datafeed):
	
	def transactionFee(self, amount: float) -> float:
		
		try:
			base_fee = self.trx_fee_base
		except:
			base_fee = 0
			
		try:
			perc_fee = self.trx_fee_perc
		except:
			perc_fee = 0
			
		return base_fee + amount * perc_fee
	
	def executeSignals(self, *args, **kwargs) -> None:
		raise(ERROR_MESSAGES['missing_method'] % (inspect.currentframe().f_code.co_name, self.__class__.__name__))
	
	def spotAction(self, *args, **kwargs) -> None:
		raise(ERROR_MESSAGES['missing_method'] % (inspect.currentframe().f_code.co_name, self.__class__.__name__))
	
	def marginAction(self, *args, **kwargs) -> None:
		raise(ERROR_MESSAGES['missing_method'] % (inspect.currentframe().f_code.co_name, self.__class__.__name__))
	
	def futuresAction(self, side:str, position_side: str, order_type: str, symbol: str, leverage: int, order_params: dict = {}) -> None:
		raise(ERROR_MESSAGES['missing_method'] % (inspect.currentframe().f_code.co_name, self.__class__.__name__))