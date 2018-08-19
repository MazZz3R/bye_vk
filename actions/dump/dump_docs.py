#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
from enum import Enum, unique

import vk_api

from actions.common import print_owner_info, get_user_dump_dir
from core.auth import get_session
from core.download import download_all_photos, download_docs, escape
from core.vk_wrapper import VkToolsWithRetry


@unique
class DocType(Enum):
    TEXT = 1
    ARCHIVE = 2
    GIF = 3
    IMAGE = 4
    AUDIO = 5
    VIDEO = 6
    BOOK = 7
    UNKNOWN = 8


def dump_docs():
    """Выгрузить документы"""

    vk_session = get_session()
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    tools = VkToolsWithRetry(vk_session)

    owner = vk_session.method('users.get')[0]
    print_owner_info(owner)

    path = os.path.join(get_user_dump_dir(owner), 'docs')
    os.makedirs(path, exist_ok=True)

    url_to_docpath = dict()

    for doc_type in list(DocType):
        doc_name = doc_type.name.lower()
        doc_idx = doc_type.value
        print(f'Получаем документы типа {doc_name}')

        docs = tools.get_all('docs.get', 2000, {
            'type': doc_idx,
            'owner_id': owner['id']
        })
        print(f'Всего {docs["count"]:d} документов')
        with open(os.path.join(path, doc_name + '.json'), 'w', encoding='utf-8') as f:
            json.dump(docs, f, separators=(',', ':'), ensure_ascii=False)

        doc_path = os.path.join(path, doc_name)

        filename_url = dict()
        for doc in docs['items']:
            filename = doc['title']
            filename_appeared = filename in filename_url
            filename = escape(filename, with_hash=filename_appeared)

            if filename.split('.')[-1] != doc['ext']:
                filename += '.' + doc['ext']

            filename_url[filename] = doc['url']

        url_list = [(url, filename, '') for filename, url in filename_url.items()]
        url_to_docpath.update(download_docs(url_list, doc_path, doc_name))
