from random import randint
from vk_api import VkApi
from group_info import group_token, group_id
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

authorize = VkApi(token=group_token)
vk = authorize.get_api()
bot_longpoll = VkBotLongPoll(authorize, group_id=group_id)
print('Bot started')
for event in bot_longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get('text'):
        received_message = event.message.get('text')
        command = received_message.lower().partition(' ')[0]
        sender = event.message.get('peer_id')
        message_id = event.message['conversation_message_id']
        print('New message!')
        print(f'Chat peer ID: {sender}')
        print(f'Message text: {received_message}')
        print(f'Conversation message ID: {message_id}\n')
        if command == 'hi':
            vk.messages.send(peer_id=sender, message='Hello World', random_id=get_random_id())
        elif command == 'emoji':
            vk.messages.send(peer_id=sender, message=f'&#{randint(128510, 128520)};', random_id=get_random_id())
        elif command == 'sticker':
            vk.messages.send(peer_id=sender, sticker_id=randint(49, 96), random_id=get_random_id())
        elif command == 'creator':
            vk.messages.send(peer_id=sender, message="Creator - onyx", random_id=get_random_id())
        elif command == 'coinflip':
            coin_side = "tails" if randint(0, 1) else "heads"
            vk.messages.send(peer_id=sender, message=coin_side, random_id=get_random_id())
        elif command == 'goodbye':
            vk.messages.send(peer_id=sender, message="bb", random_id=get_random_id())
            break;
print("Bot stopped")