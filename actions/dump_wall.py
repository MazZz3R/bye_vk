#!/usr/bin/python3
#  -*- coding: utf-8 -*-
import json
import os
from pprint import pprint

import vk_api

from actions.common import print_owner_info, ger_user_folder
from core.auth import get_session
from core.download import download_all_photos


def dump_wall():
    """Выгрузить стену"""

    vk_session = get_session()
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    tools = vk_api.VkTools(vk_session)

    """ VkTools.get_all позволяет получить все объекты со всех страниц.
        Соответственно get_all используется только если метод принимает
        параметры: count и offset.
        Например может использоваться для получения всех постов стены,
        всех диалогов, всех сообщений, etc.
        При использовании get_all сокращается количество запросов к API
        за счет метода execute в 25 раз.
        Например за раз со стены можно получить 100 * 25 = 2500, где
        100 - максимальное количество постов, которое можно получить за один
        запрос (обычно написано на странице с описанием метода)
    """

    owner = vk_session.method('users.get')[0]
    my_id = owner['id']
    print_owner_info(owner)

    path = './dumps/' + ger_user_folder(owner) + '/wall/'
    os.makedirs(path, exist_ok=True)

    print('Получаем стену...')
    wall = tools.get_all('wall.get', 100, {'owner_id': my_id})
    # TODO offsets
    print('Всего записей: ', wall['count'])

    if wall['count']:
        print('First post:')
        pprint(wall['items'][0])

    if wall['count'] > 1:
        print('\nLast post:')
        pprint(wall['items'][-1])

    wall_path = os.path.join(path, 'wall.json')
    with open(wall_path, 'w', encoding='utf-8') as f:
        json.dump(wall, f, separators=(',', ':'), ensure_ascii=False)

    download_all_photos(path, wall)
