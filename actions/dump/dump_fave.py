#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

import vk_api

from actions.common import print_owner_info, FAVE_TYPES, get_user_dump_dir
from core.auth import get_session
from core.download import download_all_photos
from core.vk_wrapper import VkToolsWithRetry


def dump_fave():
    """Выгрузить закладки"""

    vk_session = get_session()
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    tools = VkToolsWithRetry(vk_session)

    owner = vk_session.method('users.get')[0]
    print_owner_info(owner)

    path = os.path.join(get_user_dump_dir(owner), 'fave')
    os.makedirs(path, exist_ok=True)

    for fave_type in FAVE_TYPES:
        print('Получаем закладки %s...' % fave_type)
        fave = tools.get_all('fave.get' + fave_type, 100)
        print('Всего %d %s' % (fave['count'], fave_type))

        json_path = os.path.join(path, fave_type.lower() + '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(fave, f, separators=(',', ':'), ensure_ascii=False)

        download_all_photos(path, fave, 'закладок')
