import asyncio
import requests

from telethon import TelegramClient, functions, types
from telethon.tl.types import PeerChannel
from telethon.tl.functions.messages import SendReactionRequest

api_id = 26062203
api_hash = 'f1cd7f14a6ec31efad6290400891a8d4'
session_name = 'anon'
client = TelegramClient(session_name, api_id, api_hash)
test_group_name = 'https://t.me/+dnN1dTHuKvtiYzVi'
bot_token = '6012872667:AAGsHn6v9vojwCiLLgSOy1KYoClW-auRFfM'
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

async def main():
    test_group = await client.get_entity(test_group_name)
    all_message_ids = [x.id for x in await client.get_messages(test_group, 1000)]
    print(all_message_ids)
    await client.delete_messages(test_group, all_message_ids)

    await client.send_message(test_group, 'Test message 1')
    
   
    
    await client.send_message(test_group, 'Test message 2')
    await client.send_message(test_group, 'Test message 3')
    last_message = await client.get_messages(test_group)
    print(last_message[0].id)
    print(test_group.id)
    bot_payload = {
        'chat_id': -1001970114624,
        'text': 'test_reply',
        'reply_to_message_id': last_message[0].id
    }
    reply = requests.get('https://api.telegram.org/bot6012872667:AAGsHn6v9vojwCiLLgSOy1KYoClW-auRFfM/sendMessage', params=bot_payload)
    print(reply.json())

with client:
    client.loop.run_until_complete(main())