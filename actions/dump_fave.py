#!/usr/bin/python3
#  -*- coding: utf-8 -*-
import json
import os
from pprint import pprint

import vk_api

from actions.common import print_owner_info
from core.download import download_all_photos
from core.auth import get_session


def dump_fave():
    """Выгрузить закладки"""

    vk_session = get_session()
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    tools = vk_api.VkTools(vk_session)

    owner = vk_session.method('users.get')[0]
    print_owner_info(owner)

    path = './dumps/{0} {1} [{2}]/fave/'.format(
        owner['first_name'], owner['last_name'], owner['id'])
    os.makedirs(path, exist_ok=True)

    types = ['Photos', 'Posts', 'Videos', 'Users', 'Links', 'MarketItems']
    for fave_type in types:
        print('Получаем закладки %s...' % fave_type)
        fave = tools.get_all('fave.get' + fave_type, 100)
        # TODO offsets
        print('Всего записей: ', fave['count'])

        json_path = os.path.join(path, fave_type.lower() + '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(fave, f, separators=(',', ':'), ensure_ascii=False)

        download_all_photos(path, fave)
