from telethon import TelegramClient

api_id = 26062203
api_hash = 'f1cd7f14a6ec31efad6290400891a8d4'

with TelegramClient('anon', api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))