import typing as t
from pandas import DataFrame

class Priceframe:
	
	_required_columns: set = {'time', 'open', 'high', 'low', 'close', 'volume'}
	_priceframe: DataFrame = None
	
	def __init__(self, df: t.Optional[DataFrame] = None) -> None:
		if df is not None:
			self.set(df)
	
	def set(self, df: DataFrame) -> None:
		for req_col in self._required_columns:
			if req_col not in df.columns:
				raise Exception(f'Missing required column "{req_col}"')
				
		self._priceframe = df
	
	def get(self) -> DataFrame:
		return self._priceframe
	