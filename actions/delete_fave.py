#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import time

from actions.common import are_you_sure, print_owner_info, FAVE_TYPES
from core.auth import get_session

try:
    import simplejson as json
except ImportError:
    import json

import vk_api


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

    for fave_type in FAVE_TYPES :
        print('Получаем закладки %s...' % fave_type)
        fave = vk_tools.get_all('fave.get' + fave_type, 100)
        # TODO offsets
        print('Всего %d %s' % (fave['count'], fave_type))

        if fave['count'] == 0:
            print("Нет " + fave_type)
            continue

        sure = are_you_sure()
        if not sure:
            continue

        if fave_type in ['Photos', 'Posts', 'Videos']:
            for item in fave['items']:
                values = {
                    'type': fave_type.lower()[:-1],
                    'owner_id': item['owner_id'],
                    'item_id': item['id']
                }
                print('Удаляем %s...' % values)
                try:
                    vk_session.method('likes.delete', values=values)
                except vk_api.ApiError:
                    print('Ошибка')
                time.sleep(1)
        else:
            sys.stderr.write('Ещё не готово. Удалите %s вручную, пожалуйста'
                             '\n' % fave_type)
