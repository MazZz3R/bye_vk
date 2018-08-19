#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
import time

from actions.common import are_you_sure, print_owner_info, FAVE_TYPES, pluralize
from core.auth import get_session

try:
    import simplejson as json
except ImportError:
    import json

import vk_api

TIMEOUT_FOR_UNLIKE = 1
TIMEOUT_DELTA = 15


def delete_fave():
    """Удалить закладки (лайки)"""

    vk_session = get_session()

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk_tools = vk_api.VkTools(vk_session)

    owner = vk_session.method('users.get')[0]
    print_owner_info(owner)

    for fave_type in FAVE_TYPES:
        print('Получаем закладки %s...' % fave_type)
        fave = vk_tools.get_all('fave.get' + fave_type, 100)
        cnt = fave['count']
        fave_types = fave_type + 's'
        print(f'Всего {cnt:d} '
              f'{pluralize(cnt, fave_type, fave_types, fave_types)}')

        if cnt == 0:
            print("У Вас нет " + fave_type)
            continue

        sure = are_you_sure()
        if not sure:
            continue

        mode = input(
            'При удалении лайков часто выскакивает капча. Выберите режим:\n'
            '[+] агрессивный (1 лайк в ' + str(TIMEOUT_FOR_UNLIKE) +
            ' сек, капча каждые 14-18 объектов)\n'
            '[-] аккуратный (капча каждые 45-50 объектов)')
        aggressive = mode == '+'

        if fave_type in ['Photos', 'Posts', 'Videos']:
            for item in fave['items']:
                values = {
                    'type': fave_type.lower()[:-1],
                    'owner_id': item['owner_id'],
                    'item_id': item['id']
                }
                print('Удаляем %s...' % values)
                vk_session.method('likes.delete', values=values)

                timeout = TIMEOUT_FOR_UNLIKE
                if not aggressive:
                    timeout += random.random() * TIMEOUT_DELTA
                time.sleep(timeout)
        else:
            print(f'Ещё не готово. Удалите {fave_type} вручную, пожалуйста\n')
    print('API вконтакте не позволяет удалять лайки с объектов удалённых '
          'групп или пользователей. Пожалуйста, просмотрите вручную закладки '
          'и снимите лайки.')
