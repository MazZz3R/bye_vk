#!/usr/bin/python3
# -*- coding: utf-8 -*-
from actions.common import are_you_sure, print_owner_info, pluralize
from core.auth import get_session

try:
    import simplejson as json
except ImportError:
    import json

import vk_api

TIMEOUT_FOR_DELETE = 1
TIMEOUT_DELTA = 15


def delete_docs():
    """Удалить документы"""

    vk_session = get_session()

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk_tools = vk_api.VkTools(vk_session)

    owner = vk_session.method('users.get')[0]
    print_owner_info(owner)

    docs = vk_tools.get_all('docs.get', 2000)
    cnt = docs["count"]
    if cnt == 0:
        print("У Вас нет документов")
        return
    else:
        print(f"У Вас {cnt:d} "
              f"{pluralize(cnt, 'документ', 'документа', 'документов')}")

    sure = are_you_sure()
    if not sure:
        return

    for doc in docs['items']:
        print('Удаляем %s...' % doc['title'])
        vk_session.method('docs.delete', values={
            'owner_id': owner['id'],
            'doc_id': doc['id']
        })
