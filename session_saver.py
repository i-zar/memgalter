from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 26062203
api_hash = 'f1cd7f14a6ec31efad6290400891a8d4'

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())