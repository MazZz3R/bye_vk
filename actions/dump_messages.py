#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from core.download import download_all_photos
from core.auth import get_session

try:
    import simplejson as json
except ImportError:
    import json

import vk_api


def dump_messages():
    """Выгрузить сообщения (до нескольких часов)"""

    vk_session = get_session()

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk_tools = vk_api.VkTools(vk_session)

    owner = vk_session.method('users.get')[0]
    print('My page: http://vk.com/id{}'.format(owner['id']))

    path = './dumps/dialogs/{0} {1} [{2}]/'.format(owner['first_name'], owner['last_name'], owner['id'])
    os.makedirs(path, exist_ok=True)

    print('Get dialogs...')
    dialogs = vk_tools.get_all(
        'messages.getDialogs',
        max_count=200,
        values={'preview_length': '0'}
    )

    print('Dialogs count:', dialogs['count'])

    for item in dialogs['items']:
        item = item['message']

        if 'chat_id' in item:
            user_id = 2000000000 + item['chat_id']
        else:
            user_id = item['user_id']

        print('Get messages %s...' % user_id)

        values = {
            'user_id': user_id,
            'rev': '1'
        }

        messages = vk_tools.get_all(
            'messages.getHistory',
            max_count=200,
            values=values
        )
        messages['id'] = user_id
        messages['owner'] = owner
        messages['users'] = get_user_avatars(messages, user_id, vk_session)

        dialog_path = os.path.join(path, str(user_id))
        os.makedirs(dialog_path, exist_ok=True)

        with open(os.path.join(dialog_path, 'im.json'), 'w', encoding='utf-8') as f:
            json.dump(messages, f, separators=(',', ':'), ensure_ascii=False)

        download_all_photos(dialog_path, messages)


def get_user_avatars(messages, user_id, vk_session):
    user_ids = set()
    user_ids.add(user_id)
    for item_ in messages['items']:
        if not item_['from_id'] in user_ids:
            user_ids.add(item_['from_id'])

        for f in item_.get('fwd_messages', []):
            if not f['user_id'] in user_ids:
                user_ids.add(f['user_id'])
    values = {
        'user_ids': ','.join(str(i) for i in user_ids),
        'fields': 'photo_50'
    }
    response = vk_session.method('users.get', values=values)
    users = dict()
    for id_avatar in response:
        users.update({str(id_avatar['id']): id_avatar})
    return users
