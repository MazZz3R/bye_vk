#!/usr/bin/python3
#  -*- coding: utf-8 -*-
import json
import os
from pprint import pprint

import vk_api

from core.download import download_all_photos
from core.auth import get_session


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
    print('My page: http://vk.com/id{}'.format(owner['id']))

    path = './dumps/wall/{0} {1} [{2}]/'.format(owner['first_name'], owner['last_name'], owner['id'])
    os.makedirs(path, exist_ok=True)

    print('Get wall...')
    wall = tools.get_all('wall.get', 100, {'owner_id': my_id})

    print('Posts count:', wall['count'])

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
