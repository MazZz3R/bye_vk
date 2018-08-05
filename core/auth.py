import configparser
from getpass import getpass

import vk_api

CONFIG_FILE_PATH = 'credentials.ini'


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


def get_session():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    section = config['DEFAULT']

    if 'Login' in section and 'Password' in section and \
            section['Login'] and section['Password']:
        login = section['Login']
        password = section['Password']
    else:
        login = input('Login: ')
        password = getpass()
        config['DEFAULT'] = {
            'Login': login,
            'Password': password
        }
        with open(CONFIG_FILE_PATH, 'w') as configfile:
            config.write(configfile)

    vk_session = vk_api.VkApi(
        login, password,
        auth_handler=auth_handler
    )
    return vk_session
