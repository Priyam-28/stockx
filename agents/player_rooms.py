# agents/player_rooms.py
import random
import time
import threading
from config import ASSET_CONFIG
class PlayerRoom:
    def __init__(self, market, room_id):
        self.market = market
        self.room_id = room_id

    def simulate_activity(self):
        while True:
            symbol = random.choice(ASSET_CONFIG['stable_coins'])
            action = random.choice(['buy', 'sell'])
            amount = random.randint(1, 100)
            self.market.record_activity(symbol, action, amount)
            time.sleep(random.randint(10, 30))