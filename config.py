import os
from dotenv import load_dotenv
load_dotenv()

# Discord Configuration
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

DISCORD_CHANNEL_IDS = [1346527622720520225]  # Replace with your channel IDs

if not DISCORD_BOT_TOKEN:
    raise ValueError("Discord bot token not found in .env file")
# Market Configuration
ASSET_CONFIG = {
    'meme_coins': {
        'DOGE2': {'base_price': 0.10, 'volatility': 0.2},
        'SHIB3': {'base_price': 0.05, 'volatility': 0.3}
    },
    'stable_coins': ['USDS', 'EURO-S'],
    'traditional_assets': {
        'BTC-SIM': {'ticker': 'BTC-USD'},
        'TECH-ETF': {'ticker': 'SPY'}
    }
}

# Simulation Parameters
PRICE_UPDATE_INTERVAL = 60  # Seconds
ACTIVITY_IMPACT_FACTOR = 0.0001