from datafeed.exchanges._Exchanges import _Exchanges
import typing as t
from core.Signal import Signal

class Binance(_Exchanges):
	
	trx_fee_perc: float = 0.001
	
	def executeSignals(self, signals: t.List[Signal]) -> None:
		pass
	
	def spotAction(self, side:str, position_side: str, order_type: str, symbol: str, order_params: dict = {}) -> None:
		pass
	
	def marginAction(self, side:str, position_side: str, order_type: str, symbol: str, leverage: int, order_params: dict = {}) -> None:
		pass
	
	def futuresAction(self, side:str, position_side: str, order_type: str, symbol: str, leverage: int, order_params: dict = {}) -> None:
		pass
	
	