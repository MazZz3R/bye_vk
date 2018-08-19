import datetime
import json
import os
import platform
import shutil
import sys
import threading
from urllib.request import urlopen, Request
from uuid import getnode as get_mac

from core.path_helper import data_path
from settings import VERSION, CLIENT, PY_INSTALLER

FIREBASE_URL = 'https://byevk0.firebaseio.com/'
GET_LATEST_VERSION = f'{FIREBASE_URL}/latest_version.json'
GET_LATEST_EXE_URL = f'{FIREBASE_URL}/latest_exe.json'
LAUNCHED_FILE = data_path('.launched')

WELCOME_MESSAGE = '''
               ____
              /\   \            Bye, vk!
             /  \   \\
            /    \   \\        ver. %s
           /      \   \\
          /   /\   \   \\
         /   /  \   \   \\
        /   /    \   \   \\
       /   /    / \   \   \\
      /   /    /   \   \   \\
     /   /    /---------'   \\
    /   /    /_______________\\    
    \  /                     /
     \/_____________________/
'''

UPDATE_MESSAGE = '''
                     ,---.           ,---.
                    / /"`.\.--"""--./,'"\ \\
                    \ \    _       _    / /
                     `./  / __   __ \  \,'
                      /    /_O)_(_O\    \\
                      |  .-'  ___  `-.  |
                   .--|       \_/       |--.
                 ,'    \   \   |   /   /    `.
                /       `.  `--^--'  ,'       \\
             .-"""""-.    `--.___.--'     .-"""""-.
.-----------/         \------------------/         \--------------.
| .---------\         /----------------- \         /------------. |
| |          `-`--`--'                    `--'--'-'             | |
| |               Привет, дружочек-пирожочек!                   | |
| |                                                             | |
| |          Доступна новая версия Bye, vk! v.%s
%s
| |_____________________________________________________________| |
|_________________________________________________________________|
                   )__________|__|__________(
                  |            ||            |
                  |____________||____________|
                    ),-----.(      ),-----.(
                  ,'   ==.   \    /  .==    `.
                 /            )  (            \\
                 `==========='    `===========' 
'''

UPDATE_INSTRUCTION_EXE = (
    '| |      Нажми "+", чтобы я скачал и запустил новую версию      | |'
)

UPDATE_INSTRUCTION_PY = (
    '| |          Чтобы обновиться, выйди, сделай git pull           | |\n'
    '| |                и запусти bye_vk.py заново                   | |'
)


def resize_cmd():
    import subprocess
    subprocess.Popen('mode con: cols=120 lines=40', shell=True)


def print_welcome():
    print(WELCOME_MESSAGE % VERSION)


def send_stats():
    base_url = '%s/users/%s/' % (FIREBASE_URL, get_mac())
    now = str(datetime.datetime.utcnow()).split('.')[0]
    payload = {now: VERSION + '-' + CLIENT}

    if not os.path.isfile(LAUNCHED_FILE):
        url = base_url + 'first_launch.json'
        os.makedirs(data_path('.'), exist_ok=True)
        open(LAUNCHED_FILE, 'a').close()
    else:
        url = base_url + 'launches.json'

    req = Request(url,
                  data=json.dumps(payload).encode('utf8'),
                  headers={'content-type': 'application/json'})
    req.get_method = lambda: 'PATCH'
    # Not in the MainThread!
    threading.Thread(target=urlopen, args=(req,), daemon=True).start()


def check_update():
    is_exe = PY_INSTALLER and platform.system() == 'Windows'
    if is_exe:
        resize_cmd()

    # Determine whether people use this application
    send_stats()
    try:
        response = urlopen(GET_LATEST_VERSION)
        if response.status == 200:
            latest_version = response.read().decode('utf-8').strip('"')
            if latest_version <= VERSION:
                return

            update_msg = UPDATE_INSTRUCTION_EXE if PY_INSTALLER \
                else UPDATE_INSTRUCTION_PY
            print(UPDATE_MESSAGE % (
                latest_version + ' ' * (18 - len(latest_version)) + '| |',
                update_msg
            ))
            if is_exe:
                answer = input('> ')
                if answer != '+':
                    return

                response_exe = urlopen(GET_LATEST_EXE_URL)
                if response_exe.status != 200:
                    print('Что-то пошло не так при скачивании exe')
                    return
                exe_url = response_exe.read().decode('utf-8').strip('"')
                filename = 'bye_vk.' + latest_version + '.exe'
                with urlopen(exe_url) as exe, open(filename, 'wb') as f:
                    shutil.copyfileobj(exe, f)
                # subprocess.Popen('cmd /K ' + filename, shell=True)
                os.system('start cmd /K ' + filename)
                sys.exit(0)
            else:
                input('Нажми <Enter>, чтобы продолжить\n')
    except Exception as ex:
        print(ex)
        print('Что-то пошло не так при обновлении')
