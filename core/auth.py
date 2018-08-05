import configparser
from getpass import getpass

import vk_api


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def get_session():
    config = configparser.ConfigParser()

    if 'Login' in config['DEFAULT'] and 'Password' in config['DEFAULT']:
        login = config['DEFAULT']['Login']
        password = config['DEFAULT']['Password']
    else:
        login = input('Login: ')
        password = input('Password: ')  # FIXME getpass

    vk_session = vk_api.VkApi(
        login, password,
        auth_handler=auth_handler  # функция для обработки двухфакторной аутентификации
    )
    # vk_session = vk_api.VkApi(login, password)
    return vk_session
