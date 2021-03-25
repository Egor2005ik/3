import asyncio
import warnings

import typing

from loguru import logger
from python_rucaptcha import ImageCaptcha
from vkbottle import VKError
from vkbottle.api import API
from vkbottle.api.api.error_handler import VKErrorHandler
from vkbottle.http import HTTPRequest
from vkbottle.utils import json

from const import DEFAULT_CONFIG, APPS

request = HTTPRequest()


class ErrorHandler(VKErrorHandler):

    async def unhandled_error(self, e: VKError):
        raise e


def read_config() -> dict:
    try:
        with open('config.json', 'r', encoding='utf-8') as file:
            return json.loads(file.read())
    except FileNotFoundError:
        write_config(DEFAULT_CONFIG)
        warnings.warn("ДБ не найдена, создал новую")
        return DEFAULT_CONFIG


def write_config(_config: dict):
    with open('config.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(_config, ensure_ascii=False, indent=2))


async def rps_error_handler(e: VKError):
    await asyncio.sleep(1)
    return await e.method_requested(**e.params_requested)


async def solve_captcha(e: VKError):
    ru_captcha_key = "54806b4220ce3927c9164aec11101087"

    user_answer = ImageCaptcha. \
        ImageCaptcha(rucaptcha_key=ru_captcha_key). \
        captcha_handler(captcha_link=e.raw_error['captcha_img'])

    if not user_answer['error']:
        logger.info("Каптча решена")
        return user_answer['captchaSolve']


async def get_tokens(_login: str, _password: str, limit: int = 3) -> typing.List[str]:
    _tokens: typing.List[str] = []
    for k, v in APPS.items():
        response = await request.get(
            "https://oauth.vk.com/token"
            "?grant_type=password"
            f"&client_id={v['client_id']}"
            f"&client_secret={v['client_secret']}"
            f"&username={_login}"
            f"&password={_password}"
        )
        if "error" in response:
            raise VKError(0, response["error_description"])
        if len(_tokens) < limit:
            _tokens.append(response["access_token"])
    return _tokens


async def get_spam_apis() -> typing.List[API]:
    config = read_config()
    apis: typing.List[API] = []
    for token in config['tokens']:
        api = API(token)
        api.error_handler = ErrorHandler()
        api.error_handler.add_error_handler(6, rps_error_handler)
        api.error_handler.captcha_handler(solve_captcha)
        apis.append(api)

    for log_pass_dict in config['log_pass']:
        api = API(await get_tokens(log_pass_dict['login'], log_pass_dict['password']))
        api.error_handler = ErrorHandler()
        api.error_handler.add_error_handler(6, rps_error_handler)
        api.error_handler.captcha_handler(solve_captcha)
        apis.append(api)
    return apis


def check_access(user_id: int) -> bool:
    config = read_config()
    if user_id in config['admin_ids']:
        return True
    return False
