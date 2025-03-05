import threading
from market.core import GlobalMarket
from discord_bot.meme_tracker import MemeTracker
from agents.player_rooms import PlayerRoom
from dashboard.app import app
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

def main():
    # Initialize market
    market = GlobalMarket()
    
    # Start price updates in a separate thread
    market_thread = threading.Thread(target=market.update_prices, daemon=True)
    market_thread.start()
    
    # Start player rooms in separate threads
    for i in range(3):  # Start 3 player rooms
        room = PlayerRoom(market, i)
        room_thread = threading.Thread(target=room.simulate_activity, daemon=True)
        room_thread.start()
    
    # Start Discord bot in a separate thread
    bot = MemeTracker(market)
    bot_thread = threading.Thread(target=bot.run, args=(DISCORD_BOT_TOKEN,), daemon=True)
    bot_thread.start()
    
    # Start Flask server
    app.run(host="0.0.0.0", port=8050, debug=False)  # Disable debug mode for production

if __name__ == "__main__":
    main()