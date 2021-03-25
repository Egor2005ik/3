from typing import Optional

from vkbottle import Message
from vkbottle.framework.blueprint.user import Blueprint
from vkbottle.framework.framework.rule import FromMe

from utils import read_config, write_config, check_access

user = Blueprint()


@user.on.message_handler("/добавить акк <login> <password>")
async def add_account(message: Message, login: str, password: str) -> Optional[str]:
    if not check_access(message.from_id):
        return
    config = read_config()
    config['log_pass'].append({
        'login': login, 'password': password
    })
    write_config(config)
    return "Логин и пароль добавлен"


@user.on.message_handler("/добавить токен <token>")
async def add_token(message: Message, token: str) -> Optional[str]:
    if not check_access(message.from_id):
        return
    config = read_config()
    config['tokens'].append(token)
    write_config(config)
    return "Токен добавлен"
