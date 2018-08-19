#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import vk_api

from actions.common import print_owner_info, FAVE_TYPES, get_user_dump_dir, append_to_json
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
        new_count = fave['count']
        print('Всего %d %s' % (new_count, fave_type))

        json_path = os.path.join(path, fave_type.lower() + '.json')
        fave = append_to_json(json_path, fave, 'id')
        all_count = len(fave["items"])
        if new_count != all_count:
            print(f'Всего {len(fave["items"])} с уже скачанными закладками')
        download_all_photos(path, fave, 'закладок')
