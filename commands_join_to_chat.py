import asyncio
from typing import Optional

from vkbottle import Message, VKError
from vkbottle.framework.blueprint.user import Blueprint
from vkbottle.framework.framework.rule import FromMe

from spammer import spammer
from utils import get_spam_apis, check_access

user = Blueprint()

loop = asyncio.get_event_loop()

CHAT_SPAM_STATE = {'working': False}


def get_state():
    return CHAT_SPAM_STATE


@user.on.message_handler('/беседа старт <link> <text>')
async def wrapper(message: Message, link: str, text: str) -> Optional[str]:
    if not check_access(message.from_id):
        return
    spam_database = []

    CHAT_SPAM_STATE.update({'working': True})
    for api in await get_spam_apis():
        
        try:

            spam_database.append((api, (await api.messages.join_chat_by_invite_link(link=link)).chat_id + 2e9,))
        except VKError:
            pass

    for account_info in spam_database:
        loop.create_task(spammer(account_info[0], account_info[1], text, lambda: get_state()))

    return "Расчет придурков окончен"


@user.on.message_handler('/беседа стоп')
async def wrapper(message: Message):
    if not check_access(message.from_id):
        return
    CHAT_SPAM_STATE.update({'working': False})


@user.on.message_handler('/беседа вход <link>')
async def wrapper(message: Message, link: str) -> Optional[str]:
    if not check_access(message.from_id):
        return
    spam_database = []

    CHAT_SPAM_STATE.update({'working': True})
    for api in await get_spam_apis():

        try:
            spam_database.append((api, (await api.messages.join_chat_by_invite_link(link=link)).chat_id + 2e9,))
        except VKError:
            pass
    return "Вход выполнен мой господин начинаем ебать их "
