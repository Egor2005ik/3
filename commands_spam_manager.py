import asyncio
from typing import Optional

from vkbottle import Message
from vkbottle.framework.blueprint.user import Blueprint
from vkbottle.framework.framework.rule import FromMe

from spammer import spammer
from utils import get_spam_apis, check_access

user = Blueprint()

loop = asyncio.get_event_loop()

SPAM_STATE = {}


def get_state():
    return SPAM_STATE


@user.on.message_handler("/старт [id<user_id:int>|<user_name>] <text>")
async def run_spam_handler(message: Message, user_id: int, text: str, **kwargs) -> Optional[str]:
    if not check_access(message.from_id):
        return
    global loop
    target_user = (await message.api.users.get(user_ids=user_id))[0]

    apis = await get_spam_apis()

    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    SPAM_STATE.update({"working": True})

    for api in apis:
        loop.create_task(spammer(api, target_user.id, text, lambda: get_state()))

    if not loop.is_running():
        loop.run_forever()

    return f"наначали ебать " \
           f"[id{target_user.id}|{target_user.first_name} {target_user.last_name}]"


@user.on.message_handler("/стоп")
async def stop_spam_handler(message: Message):
    if not check_access(message.from_id):
        return
    SPAM_STATE.update({'working': False})
    return "выебал"

