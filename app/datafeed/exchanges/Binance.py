from datafeed.exchanges._Exchanges import _Exchanges
import typing as t

class Binance(_Exchanges):
	
	trx_fee_perc: float = 0.001
	
	def analysePrice(self, side:str, position_side: str, strategy):
		pass
	
	def triggerSpotAction(self, side:str, position_side: str, order_type: str, symbol: str, order_params: dict = {}) -> t.Any:
		pass
	
	