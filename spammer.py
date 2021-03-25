import asyncio
import time
from typing import Callable

from loguru import logger
from vkbottle import VKError
from vkbottle.api import API


async def spammer(
        api: API,
        target_id: int,
        text: str,
        state: Callable,
        *,
        attachments: str = "",
        start_time: int = time.time()
):
    user = (await api.users.get())[0]
    messages = 0
    while True:
        if not state()['working']:
            break
        try:
            await api.messages.send(peer_id=target_id, random_id=0, message=text, attachment=attachments)
        except VKError as ex:
            if ex.error_code == 902:
                logger.error(f"<red>{await api.user_id}</red> | Пидарас закрыл ЛС")
                break

        messages += 1

        curr_rate = round(messages / (time.time() - start_time), 2)

        if curr_rate <= 0.2:
            curr_rate_text = f"<b><red>{curr_rate} смс./сек.</red></b>"
        elif 0.2 < curr_rate <= 0.3:
            curr_rate_text = f"<b><yellow>{curr_rate} смс./сек.</yellow></b>"
        elif 0.3 < curr_rate <= 0.5:
            curr_rate_text = f"<b><green>{curr_rate} смс./сек.</green></b>"
        else:
            curr_rate_text = f"<b><fg #008000>{curr_rate} смс./сек.</fg #008000></b>"


        logger.opt(colors=True).success(
            f"<red>{user.first_name} {user.last_name}</red> | "
            f"Cмс отправлено в беседу {target_id} | "
            f"{curr_rate_text}"
        )
        await asyncio.sleep(0.1)
