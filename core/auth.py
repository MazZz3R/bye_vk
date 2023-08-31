import json
import os
import webbrowser

from core.path_helper import data_path
from core.vk_wrapper import VkApiWithRetry

VK_CONFIG_FILE = data_path('vk_config.v2.json')


def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    webbrowser.open(captcha.get_url())
    key = input("Enter captcha code: ").strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)


def get_session():
    token = None

    if os.path.exists(VK_CONFIG_FILE) and os.path.isfile(VK_CONFIG_FILE):
        try:
            with open(VK_CONFIG_FILE, 'r', encoding='utf-8') as f:
                vk_config = json.load(f)
                token = vk_config["token"]
        except (TypeError, ValueError, OSError, IOError) as ex:
            print(ex)

    if not token:
        token = input("Токен: ")
        with open(VK_CONFIG_FILE, 'w+', encoding='utf-8') as f:
            json.dump({"token": token}, f)

    return VkApiWithRetry(token=token, captcha_handler=captcha_handler)
