#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import time

import vk_api

from actions.common import print_owner_info, get_user_dump_dir
from core.auth import get_session
from core.download import download_all_photos, escape


def dump_albums():
    """Выгрузить альбомы"""

    vk_session = get_session()
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    tools = vk_api.VkTools(vk_session)

    owner = vk_session.method('users.get')[0]
    print_owner_info(owner)

    path = os.path.join(get_user_dump_dir(owner), 'albums')
    os.makedirs(path, exist_ok=True)

    albums = tools.get_all('photos.getAlbums', 1000)
    with open(os.path.join(path, 'albums.json'), 'w', encoding='utf-8') as f:
        json.dump(albums, f, separators=(',', ':'), ensure_ascii=False)

    albums['items'] += [
        {'title': 'Сохранённые фотографии', 'id': 'saved'},
        {'title': 'Фотографии со стены', 'id': 'wall'},
        {'title': 'Фотографии профиля', 'id': 'profile'}
    ]

    for album in albums['items']:
        print('Скачиваем альбом ' + album["title"])
        album_photos = tools.get_all('photos.get', 1000, values={
            'album_id': album['id']
        })
        time.sleep(1)

        album_path = os.path.join(path, f'{escape(album["title"])} [{album["id"]}]'.strip())
        os.makedirs(album_path, exist_ok=True)

        with open(os.path.join(album_path, 'album.json'), 'w', encoding='utf-8') as f:
            json.dump(album_photos, f, separators=(',', ':'), ensure_ascii=False)

        download_all_photos(album_path, album_photos, 'альбома')

        print('Получаем комменты для ' + escape(album["title"]))
        album_comments = {}
        for photo in album_photos['items']:
            comments = tools.get_all('photos.getComments', 100, values={
                'photo_id': photo['id'],
                'need_likes': 1,
                'extended': 1
            })
            time.sleep(1)
            album_comments[photo['id']] = comments

        with open(os.path.join(album_path, 'comments.json'), 'w', encoding='utf-8') as f:
            json.dump(album_comments, f, separators=(',', ':'), ensure_ascii=False)
