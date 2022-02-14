#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time

from actions.common import are_you_sure, print_owner_info, pluralize
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
        vk_session.method("users.get")
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk_tools = vk_api.VkTools(vk_session)

    owner = vk_session.method("users.get")[0]
    print_owner_info(owner)

    print("Получаем альбомы...")
    albums = vk_tools.get_all("video.getAlbums", 100)
    album_count = albums["count"]
    print(f"Всего {album_count:d} " +
          f"{pluralize(album_count, 'альбом', 'альбома', 'альбомов')}")

    videos = {
        "count": 0,
        "items": []
    }
    video_ids = set()

    for album in albums["items"]:
        album_videos = vk_tools.get_all("video.get", 200, values={
            "album_id": album["id"]
        })
        for album_video in album_videos["items"]:
            if album_video["id"] in video_ids:
                continue
            videos["count"] += 1
            videos["items"].append(album_video)
            video_ids.add(album_video["id"])
        time.sleep(1)

    videos_other = vk_tools.get_all("video.get", 200)
    for video_other in videos_other["items"]:
        if video_other["id"] in video_ids:
            continue
        videos["count"] += 1
        videos["items"].append(video_other)
        video_ids.add(video_other["id"])

    cnt = videos["count"]
    if cnt == 0:
        print("Нет видео")
    else:
        print(f"Всего {cnt:d} видео")
        sure = are_you_sure()
        if not sure:
            return

        for video in videos["items"]:
            print("Удаляем " + video["title"])
            vk_session.method("video.delete", values={
                "owner_id": video["owner_id"],
                "video_id": video["id"],
                "target_id": owner["id"]
            })
            time.sleep(1)

    for album in albums["items"]:
        print("Удаляем альбом " + album["title"])
        vk_session.method("video.deleteAlbum", values={
            "album_id": album["id"]
        })
        time.sleep(1)

    print("Возможно, у Вас остались видеозаписи, \"нарушающие авторские права\", "
          "видео от удалённых пользователей.\nИх можно удалить вручную")
