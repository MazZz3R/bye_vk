#!/usr/bin/python3
# -*- coding: utf-8 -*-
from actions.common import are_you_sure, print_owner_info
from core.auth import get_session

try:
    import simplejson as json
except ImportError:
    import json

import vk_api


def delete_wall():
    """Удалить стену"""

    vk_session = get_session()

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk_tools = vk_api.VkTools(vk_session)

    owner = vk_session.method('users.get')[0]
    print_owner_info(owner)

    print('Получаем стену...')
    wall = vk_tools.get_all('wall.get', 100, {'owner_id': owner['id']})
    print('Всего записей: ', wall['count'])

    if wall['count'] == 0:
        print("На стене нет записей!")
        return

    sure = are_you_sure()
    if not sure:
        return

    for wall_post in wall['items']:
        values = {
            'owner_id': wall_post['owner_id'],
            'post_id': wall_post['id']
        }
        print('Удаляем %s...' % values)
        vk_session.method('wall.delete', values=values)
