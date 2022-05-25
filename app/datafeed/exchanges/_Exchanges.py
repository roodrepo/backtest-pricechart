from datafeed._Datafeed import _Datafeed

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