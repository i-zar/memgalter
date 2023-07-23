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
            result = await client(functions.messages.GetMessageReactionsListRequest(
                    peer=channelusername,
                    id=message.id,
                    limit=100
                ))
            voted_users = set()
            for reaction in result.reactions:
                voted_users.add(reaction.peer_id.user_id)
            vote_count = len(voted_users)
        user_object = await client.get_entity(message.from_id)
        user_name = user_object.first_name
        if user_object.last_name:
            user_name += (' ' + user_object.last_name)
        winning_stack.update_stack(vote_count, message.id, message.date, user_name)
    print(winning_stack.get_winner())
    print(winning_stack.get_contenders())
    winner = winning_stack.get_winner()

    greeting = '''Лучший мем недели запилен {}. Мем собрал {} реакций. Поприветствуем нового Повелителя Социомемасечной!'''.format(winner['author'], winner['votes'])

    if channel_id != reporting_channel_id:
        send_channel_update(reporting_channel_id, greeting)
    else:
        send_channel_update(reporting_channel_id, greeting, winner['message_id'])

    send_channel_update(reporting_channel_id, "Еще в Топ-5 мемов недели:")
    pretendents = winning_stack.get_contenders()
    for pretendent in pretendents:
        message = '{} , реакций: {}'.format(pretendent['author'], pretendent['votes'])
        if channel_id != reporting_channel_id:
            send_channel_update(reporting_channel_id, message)
        else:
            send_channel_update(reporting_channel_id, message, pretendent['message_id'])


class WinningStack:

    def __init__(self):
        self.stack = [{'votes':0, 'message_id':0, 'timestamp':0, 'author':0}]

    def update_stack(self, votes, message_id, timestamp, author):
        if votes > self.stack[-1]['votes'] or len(self.stack) <=5:
            self.stack.append({'votes':votes, 'message_id':message_id, 'timestamp':timestamp, 'author':author})
            self.stack = sorted(self.stack, key=lambda d: d['votes'], reverse=True)
        if len(self.stack) > 5:
            self.stack = self.stack[0:5]

    def get_winner(self):
        return self.stack[0]
    
    def get_contenders(self):
        return self.stack[1:]
    
def send_channel_update(channel, message, replied_message=None):
    
    bot_payload = {'chat_id': '-100'+ str(channel), 'text': message}
    if replied_message:
        bot_payload['reply_to_message_id'] = replied_message
    reply = requests.get('https://api.telegram.org/bot6012872667:AAGsHn6v9vojwCiLLgSOy1KYoClW-auRFfM/sendMessage', params=bot_payload)
    print(reply.json())

def lambda_handler(*args):
    with client:
        client.loop.run_until_complete(main())

if __name__ == '__main__':
    lambda_handler()