from vkbottle import Message, VKError
from vkbottle.api import API
from vkbottle.framework.blueprint.user import Blueprint

from utils import get_spam_apis, read_config, write_config, check_access, get_tokens

user = Blueprint()


@user.on.message_handler("/инфо")
async def wrapper(message: Message):
    if not check_access(message.from_id):
        return

    text = ""
    apis = await get_spam_apis()
    text += f"Всего {len(apis)} аккаунтов:\n"

    for api in apis:
        spam_user = (await api.users.get())[0]
        text += f"[id{spam_user.id}|{spam_user.first_name} {spam_user.last_name}]\n"
    return text


@user.on.message_handler("/токены")
async def wrapper(message: Message):
    if not check_access(message.from_id):
        return
    config = read_config()
    text = "токены:\n"
    for i in range(0, len(config['tokens'])):
        token = config['tokens'][i]
        api = API(token)
        try:
            _tuser = (await api.users.get())[0]
            text += f"{i}. Токен [id{_tuser.id}|{_tuser.first_name} {_tuser.last_name}] проверен\n"
        except VKError:
            text += f"{i}. Токен поврежден"
            config['tokens'][i] = None

    config['tokens'] = list([token for token in config['tokens'] if token is not None])
    write_config(config)
    return text


@user.on.message_handler("/проверить акки")
async def wrapper(message: Message):
    if not check_access(message.from_id):
        return
    config = read_config()
    text = "Проверка акаунтов:\n"
    for i in range(0, len(config['log_pass'])):
        log_pass = config['log_pass'][i]
        api = API(await get_tokens(log_pass['login'], log_pass['password']))
        try:
            _tuser = (await api.users.get())[0]
            text += f"{i}. Аккаунт [id{_tuser.id}|{_tuser.first_name} {_tuser.last_name}] проверен\n"
        except VKError:
            text += f"{i}. Токен поврежден"
            config['tokens'][i] = None

    config['tokens'] = list([token for token in config['tokens'] if token is not None])
    write_config(config)
    return text
