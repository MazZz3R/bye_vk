#!/usr/bin/python3
#  -*- coding: utf-8 -*-
import json
import os
import time

import vk_api

from actions.common import print_owner_info, ger_user_folder
from core.auth import get_session
from core.download import download_all_photos


def dump_videos():
    """Выгрузить видеозаписи *только описания, ссылки"""

    vk_session = get_session()
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    tools = vk_api.VkTools(vk_session)

    owner = vk_session.method('users.get')[0]
    print_owner_info(owner)

    path = './dumps/' + ger_user_folder(owner) + '/videos/'
    os.makedirs(path, exist_ok=True)

    videos = tools.get_all('video.get', 200)
    with open(os.path.join(path, 'videos.json'), 'w', encoding='utf-8') as f:
        json.dump(videos, f, separators=(',', ':'), ensure_ascii=False)

    download_all_photos(path, videos)

    video_comments = {}
    for video in videos['items']:
        print('Retrieving comments for' + video["title"])
        comments = tools.get_all('video.getComments', 100, values={
            'video_id': video['id'],
            'need_likes': 1,
            'extended': 1
        })
        time.sleep(1)
        video_comments[video['id']] = comments

    with open(os.path.join(path, 'comments.json'), 'w', encoding='utf-8') as f:
        json.dump(video_comments, f, separators=(',', ':'), ensure_ascii=False)
