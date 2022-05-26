from datafeed.other.YahooFinance import YahooFinance
from core.Timeframe import Timeframe
import pandas as pd

def test_priceframe() -> None:
	yf = YahooFinance()
	tf = Timeframe('30m')
	pf = yf.priceframe('AAPL', tf, period= '1mo')

	assert isinstance(pf.get(), pd.DataFrame)
	assert pf.get().size > 0
	