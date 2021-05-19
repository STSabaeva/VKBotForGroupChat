import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import VK_BOT_TOKEN
import json

session = vk_api.VkApi(token=VK_BOT_TOKEN)
longpoll = VkLongPoll(session)


def get_keyboard(buts):
    global get_but
    nb = []
    color = ''
    for i in range(len(buts)):
        nb.append([])
        for k in range(len(buts[i])):
            nb[i].append(None)
    for i in range(len(buts)):
        for k in range(len(buts[i])):
            text = buts[i][k][0]
            if buts[i][k][1] == 'p':
                color = 'positive'
            elif buts[i][k][1] == 'n':
                color = 'negative'
            nb[i][k] = {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"" + "1" + "\"}",
                    "label": f"{text}"
                },
                "color": f"{color}"
            }
    first_keyboard = {
        'one_time': False,
        'buttons': nb
    }
    first_keyboard = json.dumps(first_keyboard, ensure_ascii=False).encode(
        'utf-8')
    first_keyboard = str(first_keyboard.decode('utf-8'))
    return first_keyboard


keyboard1 = get_keyboard(
    [
        [('Ссылка на сообщество', 'p')],
        [('Ссылка на обсуждения сообщества', 'p')],
        [('Ссылка на альбомы сообщества', 'p')]
    ]
)


def send_message(id, text):
    session.method('messages.send',
                   {'chat_id': id, 'message': text, 'random_id': 0,
                    'keyboard': keyboard1})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            if event.from_chat:

                msg = event.text.lower()
                id = event.chat_id

                if msg in ['мат']:
                    send_message(id, f'@{event.user_id},'
                                     f' вы нарушили правило беседы!')
