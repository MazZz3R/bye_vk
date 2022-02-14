#!/usr/bin/python3
# -*- coding: utf-8 -*-
from actions.common import are_you_sure, print_owner_info, pluralize
from core.auth import get_session
from core.vk_wrapper import VkToolsWithRetry

try:
    import simplejson as json
except ImportError:
    import json

import vk_api


def delete_wall():
    """Удалить стену"""

    vk_session = get_session()

    try:
        vk_session.method("users.get")
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk_tools = VkToolsWithRetry(vk_session)

    owner = vk_session.method("users.get")[0]
    print_owner_info(owner)

    print("Получаем стену...")
    wall = vk_tools.get_all("wall.get", 100, {"owner_id": owner["id"]})
    cnt = wall["count"]
    print(f"Всего {cnt:d} {pluralize(cnt, 'запись', 'записи', 'записей')}")

    if cnt == 0:
        print("На стене нет записей!")
        return

    sure = are_you_sure()
    if not sure:
        return

    for wall_post in wall["items"]:
        values = {
            "owner_id": wall_post["owner_id"],
            "post_id": wall_post["id"]
        }
        print(f"Удаляем {values}...")
        try:
            vk_session.method("wall.delete", values=values)
        except vk_api.AccessDenied:
            # Happens when trying to delete one post two times (dunno why)
            pass
