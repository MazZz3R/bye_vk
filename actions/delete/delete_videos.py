#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time

from actions.common import are_you_sure, print_owner_info
from core.auth import get_session

try:
    import simplejson as json
except ImportError:
    import json

import vk_api


def delete_videos():
    """Удалить видео"""

    vk_session = get_session()

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk_tools = vk_api.VkTools(vk_session)

    owner = vk_session.method('users.get')[0]
    print_owner_info(owner)

    videos = vk_tools.get_all('video.get', 200)

    if videos['count'] == 0:
        print("Нет video")
    else:
        print('Всего ' + str(videos['count']) + ' video')
        sure = are_you_sure()
        if not sure:
            return

        for video in videos['items']:
            print('Удаляем ' + video['title'])
            vk_session.method('video.delete', values={
                'owner_id': video['owner_id'],
                'video_id': video['id'],
                'target_id': owner['id']
            })
            time.sleep(1)
