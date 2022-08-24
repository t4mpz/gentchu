from discord import Intents
from gentchu import Gentchu
from database.security import BotData

bd = BotData()
intents = Intents.default()
# intents.message_content = True
client = Gentchu(intents=intents)
client.run(bd.token)

