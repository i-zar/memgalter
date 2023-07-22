import os
os.chdir("/tmp")
import requests

from datetime import datetime, timedelta, timezone

from telethon import TelegramClient, functions
from telethon.tl.types import PeerChannel
from telethon.sessions import StringSession

api_id = os.environ.get('APIID')
api_hash = os.environ.get('APIHASH')
channel_id = int(os.environ.get('MAINCHANNEL'))
reporting_channel_id = int(os.environ.get('REPORTINGCHANNEL'))
session_string = os.environ.get('TGSESSION')
client = TelegramClient(StringSession(session_string), api_id, api_hash)
bot_token = os.environ.get('BOTTOKEN')
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

async def main():

    channelusername = await client.get_entity(PeerChannel(channel_id))
    winning_stack = WinningStack()

    async for message in client.iter_messages(channelusername):
        if message.date < datetime.now(timezone.utc) - timedelta(days=7):
            break
        vote_count = 0
        if message.reactions:
            for emoji in message.reactions.to_dict()['results']:
                vote_count += emoji['count']
            print(message.reactions.to_dict())
        user_object = await client.get_entity(message.from_id)
        user_name = user_object.first_name
        if user_object.last_name:
            user_name += (' ' + user_object.last_name)
        winning_stack.update_stack(vote_count, message.id, message.date, user_name)
    print(winning_stack.winner, winning_stack.contender)

    greeting = '''Лучший мем недели запилен {}. Мем собрал {} реакций. Поприветствуем повелителя Социомемасечной!'''.format(winning_stack.winner['author'], winning_stack.winner['votes'])

    if channel_id == reporting_channel_id:
        bot_payload = {
            'chat_id': '-100'+ str(reporting_channel_id),
            'text': greeting,
            'reply_to_message_id': winning_stack.winner['message_id']
        }
    else:
        bot_payload = {
            'chat_id': '-100'+ str(reporting_channel_id),
            'text': greeting
        }
    reply = requests.get('https://api.telegram.org/bot6012872667:AAGsHn6v9vojwCiLLgSOy1KYoClW-auRFfM/sendMessage', params=bot_payload)
    print(reply.json())

class WinningStack:

    def __init__(self):
        self.winner = {'votes':0, 'message_id':0, 'timestamp':0, 'author':0}
        self.contender = {'votes':0, 'message_id':0, 'timestamp':0, 'author':0}

    def update_stack(self, votes, message_id, timestamp, author):
        if votes > self.winner['votes']:
            self.contender = self.winner.copy()
            self.winner = {'votes': votes, 'message_id': message_id, 'timestamp':timestamp, 'author': author}
        elif votes > self.contender['votes']:
            self.contender = {'votes': votes, 'message_id': message_id, 'timestamp':timestamp, 'author': author}

def lambda_handler(*args):
    with client:
        client.loop.run_until_complete(main())

if __name__ == '__main__':
    lambda_handler()