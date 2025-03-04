# main.py
import threading
from config import DISCORD_BOT_TOKEN
from market.core import GlobalMarket
from discord_bot.meme_tracker import MemeTracker
from agents.player_rooms import PlayerRoom

def main():
    # Initialize market
    market = GlobalMarket()
    
    # Start price updates
    market_thread = threading.Thread(target=market.update_prices)
    market_thread.daemon = True
    market_thread.start()
    
    # Start player rooms
    for i in range(3):
        room = PlayerRoom(market, i)
        threading.Thread(target=room.simulate_activity).start()
    
    # Start Discord bot
    bot = MemeTracker(market)
    bot.run(DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    main()