import json
import os
import webbrowser
from getpass import getpass

from core.path_helper import data_path
from core.vk_wrapper import VkApiWithRetry

VK_CONFIG_FILE = data_path('vk_config.v2.json')


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


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
    saved_login = None

    if os.path.exists(VK_CONFIG_FILE) and os.path.isfile(VK_CONFIG_FILE):
        try:
            with open(VK_CONFIG_FILE, 'r', encoding='utf-8') as f:
                vk_config = json.load(f)
                login_list = list(vk_config.keys())
                if len(login_list) > 1:
                    print('Выберите пользователя:')
                    for idx, login in enumerate(login_list):
                        print(f'{idx + 1}. {login}')
                    login_idx = int(input('Введите номер> '))
                    saved_login = login_list[login_idx - 1]
                else:
                    saved_login = login_list[0]
        except (TypeError, ValueError, OSError, IOError) as ex:
            print(ex)

    if saved_login:
        vk_session = VkApiWithRetry(
            saved_login,
            config_filename=VK_CONFIG_FILE,
            auth_handler=auth_handler,
            captcha_handler=captcha_handler)
    else:
        login = input('Логин: ')
        password = getpass('Пароль: ')
        vk_session = VkApiWithRetry(
            login, password,
            config_filename=VK_CONFIG_FILE,
            auth_handler=auth_handler,
            captcha_handler=captcha_handler
        )
    return vk_session
