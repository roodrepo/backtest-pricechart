from backtesting import Backtest, Strategy
from core.Priceframe import Priceframe
from core.Signal import Signal
import inspect
import typing as t
from default_mutable.DefaultMutable import defaultMutable
from core.ErrorMessages import ERROR_MESSAGES

LOCAL_ERROR_MESSAGES = {
	'invalid_param_choices': 'Value of %s must be one of the following: %s'
}

class _Strategy(Strategy):
	
	signals: t.List[Signal] = None
	is_live: bool = False
	market_type: str
	
	_acceptable_market_types = {'spot', 'margin', 'futures'}
	
	@classmethod
	def backtest(cls, priceframe: Priceframe, *, cash: int, commission: float, **kwargs) -> Backtest:
		return Backtest(priceframe.get(), cls, cash=cash, commission=commission, **kwargs)
	
	@classmethod
	def live(cls, priceframe, market_type: str, cash: int, commission: float, **kwargs) -> t.List[Signal]:
		
		if market_type not in cls._acceptable_market_types:
			raise Exception(LOCAL_ERROR_MESSAGES['invalid_param_choices'] % ())
		
		strat_instance = cls(data= priceframe.get(), broker= None, params={})
		strat_instance.is_live = True
		strat_instance.market_type = market_type
		strat_instance.initLive(cash, commission, **kwargs)
		
		return [] if strat_instance.signals is None else strat_instance.signals
	
	def initLive(self, cash: int, commission: float, **kwargs) -> None:
		raise(ERROR_MESSAGES['missing_method'] % (inspect.currentframe().f_code.co_name, self.__class__.__name__))
	
	@defaultMutable
	def triggerAction(self, func: t.Callable, args_action: dict = {}, args_signal: dict = {}):
		
		if self.is_live is True:
			self.addSignal(Signal(**args_action, **args_signal))
		else:
			func(**args_action)
	
	def addSignal(self, signal: Signal):
		if self.signals is None:
			self.signals = []
			
		self.signals.append(signal)
		
		