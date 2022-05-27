from backtesting import Backtest, Strategy
from backtesting.backtesting import _Broker
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
	'''Abstract parent class for all strategies'''
	
	signals: t.List[Signal] = None
	is_live: bool = False
	market: str
	live_params: dict = None
	_acceptable_markets = {'spot', 'margin', 'futures'}
	
	@classmethod
	def backtest(cls, priceframe: Priceframe, *, cash: int, commission: float, **kwargs) -> Backtest:
		'''Backtesting the strategy'''
		return Backtest(priceframe.get(), cls, cash=cash, commission=commission, **kwargs)
	
	@classmethod
	def optimize(cls, backtest: Backtest, **kwargs) -> t.Any:
		'''Optimizing parameters of the backtested strategy'''
		return backtest.optimize(**kwargs)
	
	@classmethod
	def live(cls, priceframe, market: str, cash: int, commission: float, **kwargs) -> t.List[Signal]:
		'''Using the backtested strategy for live trading signal'''
		
		if market not in cls._acceptable_markets:
			raise Exception(LOCAL_ERROR_MESSAGES['invalid_param_choices'] % ('market_type', ', '.join(cls._acceptable_markets)))
		
		if cls.enable_live is False:
			raise Exception(f'Live trading is not enabled for {cls.__name__}')
		
		# data = {
		# 	'Close': priceframe.get()['Close'].values,
		# 	'High': priceframe.get()['High'].values,
		# 	'Low': priceframe.get()['Low'].values,
		# 	'Open': priceframe.get()['Open'].values,
		# 	'Volume': priceframe.get()['Volume'].values,
		# }
		
		# bt = cls.backtest(priceframe, cash = cash, commission= commission)
		strat_instance = cls(data= priceframe.get(), broker= None, params={})
		strat_instance.is_live = True
		strat_instance.market = market
		strat_instance.live_params = {'cash': cash, 'commission': commission, **kwargs}
		strat_instance.initLive(**kwargs)
		strat_instance.next()
		
		return [] if strat_instance.signals is None else strat_instance.signals
	
	def initLive(self, cash: int, commission: float, **kwargs) -> None:
		'''Throw exception if not implemented in the strategy'''
		
		raise(ERROR_MESSAGES['missing_method'] % (inspect.currentframe().f_code.co_name, self.__class__.__name__))
	
	@defaultMutable
	def triggerAction(self, func: t.Callable, args_action: dict = {}, args_signal: dict = {}):
		'''Trigger signal on backtest or append to the signals' list for later execution'''
		
		if self.is_live is True:
			self.addSignal(Signal(market= self.market, **args_action, **args_signal))
		else:
			func(**args_action)
	
	def addSignal(self, signal: Signal):
		'''Adding signal to list'''
		
		print(signal)
		
		# Preventing the signals list from mutability across multiple instances of same object
		if self.signals is None:
			self.signals = []
			
		self.signals.append(signal)
		
		