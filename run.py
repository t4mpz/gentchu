from discord import Intents
from gentchu import Gentchu

TOKEN = "MTAwMzY4Nzc3MTYxNTAwMjY5NQ.GPpDEB.U_nPfMf7yW_3LuaOpTFciGNUUR83LO-k0oautY"

intents = Intents.default()
# intents.message_content = True
client = Gentchu(intents=intents)
client.run(TOKEN)

