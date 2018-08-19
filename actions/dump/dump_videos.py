#!/usr/bin/python3
#  -*- coding: utf-8 -*-
import json
import os
import time

import vk_api

from actions.common import print_owner_info, get_user_dump_dir, pluralize
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

    path = os.path.join(get_user_dump_dir(owner), 'videos')
    os.makedirs(path, exist_ok=True)

    print('Получаем альбомы...')
    albums = tools.get_all('video.getAlbums', 100)
    album_count = albums['count']
    print(f'Всего {album_count:d} ' +
        f'{pluralize(album_count, "альбом", "альбома", "альбомов")}')
    with open(os.path.join(path, 'albums.json'), 'w', encoding='utf-8') as f:
        json.dump(albums, f, separators=(',', ':'), ensure_ascii=False)

    videos = {
        "count": 0,
        "items": []
    }
    print('Получаем информацию о видеозаписях...')
    video_ids = set()

    for album in albums['items']:
        album_videos = tools.get_all('video.get', 200, values={
            'album_id': album['id']
        })
        for album_video in album_videos['items']:
            if album_video['id'] in video_ids:
                continue
            videos["count"] += 1
            videos["items"].append(album_video)
            video_ids.add(album_video['id'])
        time.sleep(1)

    videos_other = tools.get_all('video.get', 200)
    for video_other in videos_other['items']:
        if video_other['id'] in video_ids:
            continue
        videos["count"] += 1
        videos["items"].append(video_other)
        video_ids.add(video_other['id'])

    with open(os.path.join(path, 'videos.json'), 'w', encoding='utf-8') as f:
        json.dump(videos, f, separators=(',', ':'), ensure_ascii=False)

    print(f'Всего {videos["count"]} видеозаписей')
    download_all_photos(path, videos, 'видеозаписей')

    video_comments = {}
    for video in videos['items']:
        print('Получаем комменты для', video["title"])
        comments = tools.get_all('video.getComments', 100, values={
            'owner_id': video['owner_id'],
            'video_id': video['id'],
            'need_likes': 1,
            'extended': 1
        })
        time.sleep(1)
        video_comments[video['id']] = comments

    with open(os.path.join(path, 'comments.json'), 'w', encoding='utf-8') as f:
        json.dump(video_comments, f, separators=(',', ':'), ensure_ascii=False)
