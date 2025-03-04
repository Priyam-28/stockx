import random
import threading
import time
from typing import Dict
from config import ASSET_CONFIG, ACTIVITY_IMPACT_FACTOR, PRICE_UPDATE_INTERVAL
from market.assets import Asset
from data.yfinance_client import YFinanceClient

class GlobalMarket:
    def __init__(self):
        self.assets: Dict[str, Asset] = {}
        self.client = YFinanceClient()
        self._initialize_assets()
        self.lock = threading.Lock()
        self.player_activity = {'buy': {}, 'sell': {}}

    def _initialize_assets(self):
        # Initialize meme coins
        for symbol, config in ASSET_CONFIG['meme_coins'].items():
            self.assets[symbol] = Asset(
                symbol=symbol,
                asset_type='meme',
                price=config['base_price'],
                volatility=config['volatility']
            )

        # Initialize stablecoins
        for symbol in ASSET_CONFIG['stable_coins']:
            self.assets[symbol] = Asset(
                symbol=symbol,
                asset_type='stable',
                price=1.0
            )

        # Initialize traditional assets
        for symbol, config in ASSET_CONFIG['traditional_assets'].items():
            self.assets[symbol] = Asset(
                symbol=symbol,
                asset_type='traditional',
                price=self.client.get_initial_price(config['ticker']),
                ticker=config['ticker']
            )

    def update_prices(self):
        while True:
            self._update_meme_coins()
            self._update_stablecoins()
            self._update_traditional_assets()
            time.sleep(PRICE_UPDATE_INTERVAL)

    def _update_meme_coins(self):
        for asset in self.assets.values():
            if asset.asset_type == 'meme':
                asset.price *= (1 + asset.sentiment + random.uniform(-0.05, 0.05))
                asset.price = max(0.01, asset.price)

    def _update_stablecoins(self):
        for asset in self.assets.values():
            if asset.asset_type == 'stable':
                impact = self._calculate_activity_impact(asset.symbol)
                asset.price = max(0.95, min(1.05, asset.price + impact))

    def _update_traditional_assets(self):
        for asset in self.assets.values():
            if asset.asset_type == 'traditional':
                asset.price = self.client.get_latest_price(asset.ticker)

    def _calculate_activity_impact(self, symbol):
        with self.lock:
            buy = sum(self.player_activity['buy'].get(symbol, []))
            sell = sum(self.player_activity['sell'].get(symbol, []))
            return (buy - sell) * ACTIVITY_IMPACT_FACTOR

    def record_activity(self, symbol, action, amount):
        with self.lock:
            if symbol not in self.player_activity[action]:
                self.player_activity[action][symbol] = []
            self.player_activity[action][symbol].append(amount)