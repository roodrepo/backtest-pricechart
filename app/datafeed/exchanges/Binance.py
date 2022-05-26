from datafeed.exchanges._Exchanges import _Exchanges
import typing as t
from core.Signal import Signal

class Binance(_Exchanges):
	
	trx_fee_perc: float = 0.001
	
	def spotAction(self, signal: Signal) -> None:
		pass
	
	def marginAction(self, signal: Signal) -> None:
		pass
	
	def futuresAction(self, signal: Signal) -> None:
		pass
	
	