from datafeed._Datafeed import _Datafeed
import inspect
import typing as t

ERROR_MESSAGES: dict = {
	'missing_method': 'The method "%s" is not implemented in class %s'
}

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
	
	def triggerSpotAction(self, side:str, position_side: str, order_type: str, symbol: str, order_params: dict = {}) -> t.Any:
		raise(ERROR_MESSAGES['missing_method'] % (inspect.currentframe().f_code.co_name, self.__class__.__name__))
	
	def triggerMarginAction(self, side:str, position_side: str, order_type: str, symbol: str, leverage: int, order_params: dict = {}) -> t.Any:
		raise(ERROR_MESSAGES['missing_method'] % (inspect.currentframe().f_code.co_name, self.__class__.__name__))
	
	def triggerFuturesAction(self, side:str, position_side: str, order_type: str, symbol: str, leverage: int, order_params: dict = {}) -> t.Any:
		raise(ERROR_MESSAGES['missing_method'] % (inspect.currentframe().f_code.co_name, self.__class__.__name__))