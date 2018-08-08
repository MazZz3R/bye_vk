import configparser
import webbrowser
from getpass import getpass
from os.path import exists, isfile

from core.vk_wrapper import VkApiWithRetry

CONFIG_FILE_PATH = 'credentials.ini'
CONFIG_FILE_DEFAULT_CONTENT = '''[DEFAULT]
login = 
password = 
'''

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
    config = configparser.ConfigParser()
    if not exists(CONFIG_FILE_PATH) or not isfile(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'w') as f:
            f.write(CONFIG_FILE_DEFAULT_CONTENT)
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

    vk_session = VkApiWithRetry(
        login, password,
        auth_handler=auth_handler,
        captcha_handler=captcha_handler
    )
    return vk_session
