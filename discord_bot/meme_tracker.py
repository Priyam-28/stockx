import discord
from discord.ext import commands
from config import DISCORD_BOT_TOKEN, DISCORD_CHANNEL_IDS

class MemeTracker(commands.Bot):
    def __init__(self, market):
        intents = discord.Intents.default()
        intents.message_content = True  # Enable access to message content
        super().__init__(command_prefix='!', intents=intents)
        self.market = market

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.channel.id not in DISCORD_CHANNEL_IDS:
            return

        content = message.content.lower()
        for symbol in self.market.assets:
            if symbol.lower() in content:
                self._update_sentiment(symbol)
        
        # Decay sentiment over time
        for asset in self.market.assets.values():
            if asset.asset_type == 'meme':
                asset.sentiment *= 0.9

    def _update_sentiment(self, symbol):
        asset = self.market.assets.get(symbol)
        if asset and asset.asset_type == 'meme':
            asset.sentiment += 0.1
            asset.sentiment = min(1.0, asset.sentiment)