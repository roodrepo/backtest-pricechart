Backtest Price Chart
==========

## Requirements
Construct a trading signal/strategy system based on a S&P500 asset and run it through a backtest. Present its PnL and any relevant risk/reward metrics

## Installation:
Clone the repository on your local machine and create the docker image `docker-compose -f docker-compose.yml up --build`. 

**ATTENTION:** This will take a long time because of all the packages required. Otherwise, the final docker image is 
available for download [here](https://wetransfer.com/downloads/d9aaf92f4d6bf1dea1f98513e5083f7920220526193420/1bd793f7020ac309b47fa76f5aa73b1520220526193443/75172a). Use the command `docker load -i <path to image tar file>` to load it.

Access the Jupyter Notebook through [http://127.0.0.1:8888/notebooks/Backtest%20Bollinger%20Band.ipynb](http://127.0.0.1:8888/notebooks/Backtest%20Bollinger%20Band.ipynb). Look out for the token in the terminal window used to launch the container.

## Reflexion:
What's the point of having a standalone backtesting system? We can backtest a strategy, but it requires extra manual 
steps to migrate it to the trading system. Extra manual steps, also means greater risk of having errors and unexpected behavior.

What if the backtesting and live trading system are one? This wil reduce devops frictions between analysts 
and developer as the code and strategy back-tested is the exact same as live trading. This applies for any future updates.
Additionally, analysts can focus solely on the strategy rather than the code.

## [Jupyter Report](http://nomobot.net/Backtest.html)

## Code Architecture:
- core
  - ErrorMessages *(global error messages)*
  - Functions 
  - Priceframe *(format price data)*
  - Signal *(data used to trigger action on exchanges)*
  - Timeframe *(operations on timeframes)*
- datafeed *(pulling data platforms)*
  - exchanges *(each exchange can also act as datafeed + performing trades)*
    - Binance
    - CryptoDotCom
    - FTX
    - Nasdaq
  - other
    - YahooFinance
- notebooks
- strategies
  - BollingerBand 

## Devops Features:
- Docker
- Coverage
- Pytest
- Typed code

In the terminal, execute the command `pytest` to execute all programmed tests and avoid side effects when pushing updates

## System Features:
- Jupyter Notebook for backtesting
- Same code for backtesting and live trading
- Multi-datafeed
- Multi-exchange
- Cron jobs

## Future Improvements:
- Add cache when pulling data
- Install Sentry for debugging
- Store trades and strategy parameters in database
- Create admin user interface
- Advanced scenario testing

## Encountered Challenges:
- Vectorbt installation (issues with numba and numpy) -> *switched to backtesting.py*
- Visualization of bollinger bands within the price chart -> *remove the bandwidth and percentage from the indicator result*
- Enable python modules in Jupyter Notebook -> *add root directory in PYTHONPATH when starting container*
- Utilizing the same code for all modes (backtesting, optimization, live-trading)
- Optimized and flexible code architecture -> *Create abstract layers for skeleton and reusable methods*
- Slow internet connexion to download packages and build docker image -> *Cache packages*