from datafeed._Datafeed import _Datafeed

def test_connect() -> None:
	result = ''
	try:
		_Datafeed.connect()
	except Exception as e:
		result = e
		
	assert isinstance(result, BaseException)
	
def test_listPairs() -> None:
	result = ''
	try:
		_Datafeed.listPairs()
	except Exception as e:
		result = e
		
	assert isinstance(result, BaseException)
	
def test_priceframe() -> None:
	result = ''
	try:
		_Datafeed.priceframe()
	except Exception as e:
		result = e
		
	assert isinstance(result, BaseException)