# market/assets.py
from dataclasses import dataclass

@dataclass
class Asset:
    symbol: str
    asset_type: str
    price: float
    volatility: float = 0.0
    sentiment: float = 0.0
    ticker: str = None