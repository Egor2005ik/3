import warnings

from vkbottle import User

from commands import blueprints
from utils import read_config, rps_error_handler

if __name__ == "__main__":
    config = read_config()
    if not config['tokens'] and not config['log_pass']:
        exit("БД пустая, идиот")

    if not config['admin_token']:
        warnings.warn("И че ты сделаешь без админа, придурок?")

    user = User(tokens=config['admin_token'], debug="INFO")
    user.error_handler.add_error_handler(6, rps_error_handler)
    user.set_blueprints(*blueprints)
    user.run_polling()


