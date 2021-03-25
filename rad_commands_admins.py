from vkbottle import Message
from vkbottle.framework.blueprint.user import Blueprint
from vkbottle.framework.framework.rule import FromMe

from utils import read_config, write_config

user = Blueprint()


@user.on.message_handler(FromMe(), "/добавить админа [id<user_id:int>|<other_text>]")
async def wrapper(message: Message, user_id: int, **kwargs):
    config = read_config()
    if user_id in config['admin_ids']:
        return "Уже в списке админов"
    config['admin_ids'].append(user_id)
    write_config(config)

    new_admin = (await message.api.users.get(user_ids=user_id))[0]

    return f"Пользователь [id{new_admin.id}|{new_admin.first_name} {new_admin.last_name}] теперь админ"


@user.on.message_handler(FromMe(), "/удалить админа [id<user_id:int>|<other_text>]")
async def wrapper(message: Message, user_id: int, **kwargs):
    config = read_config()
    if user_id not in config['admin_ids']:
        return "Не списке админов"
    config['admin_ids'].remove(user_id)
    write_config(config)

    new_admin = (await message.api.users.get(user_ids=user_id))[0]

    return f"Пользователь [id{new_admin.id}|{new_admin.first_name} {new_admin.last_name}] теперь не админ"


@user.on.message_handler(FromMe(), '/кто админ')
async def wrapper(message: Message):
    config = read_config()
    admins = await message.api.users.get(user_ids=config['admin_ids'])
    text = "Админы:"

    for admin in admins:
        text += f"[id{admin.id}|{admin.first_name} {admin.last_name}]"

    return text
