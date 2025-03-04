# data/yfinance_client.py
import yfinance as yf
from config import ASSET_CONFIG

class YFinanceClient:
    def get_initial_price(self, ticker):
        data = yf.download(ticker, period='1y', interval='1d')
        return data['Close'].iloc[-1]

    def get_latest_price(self, ticker):
        data = yf.download(ticker, period='1d', interval='1m')
        return data['Close'].iloc[-1] if not data.empty else None