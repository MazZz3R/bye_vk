#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time

from actions.common import print_owner_info, ger_user_folder
from core.auth import get_session
from core.download import download_all_photos
from core.vk_wrapper import VkToolsWithRetry

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

    vk_tools = VkToolsWithRetry(vk_session)

    owner = vk_session.method('users.get')[0]
    print_owner_info(owner)

    path = './dumps/' + ger_user_folder(owner) + '/conversations/'
    os.makedirs(path, exist_ok=True)

    print('Get conversations...')
    conversations = vk_tools.get_all(
        'messages.getConversations',
        max_count=200,
        values={'preview_length': '0'}
    )

    print('Dialogs count:', conversations['count'])

    for item in conversations['items']:
        conversation = item['conversation']
        peer_id = conversation['peer']['id']
        peer_type = conversation['peer']['type']

        print('Get messages %s...' % peer_id)

        values = {
            'rev': '1'
        }

        if peer_type == 'user':
            values.update({'user_id': peer_id})
        elif peer_type == 'chat':
            values.update({'peer_id': peer_id})
        elif peer_type == 'group':  # FIXME test me
            values.update({'peer_id': peer_id})
        elif peer_type == 'email':  # FIXME test me
            values.update({'peer_id': peer_id})  # or conversation['peer']['local_id']})

        messages = vk_tools.get_all(
            'messages.getHistory',
            max_count=200,
            values=values
        )
        time.sleep(1)
        messages['id'] = peer_id
        messages['owner'] = owner
        messages['users'] = get_user_avatars(messages, peer_id, vk_session)

        dialog_path = os.path.join(path, str(peer_id))
        os.makedirs(dialog_path, exist_ok=True)

        with open(os.path.join(dialog_path, 'im.json'), 'w', encoding='utf-8') as f:
            json.dump(messages, f, separators=(',', ':'), ensure_ascii=False)

        download_all_photos(dialog_path, messages, 'диалога')


def get_user_avatars(messages, user_id, vk_session):
    user_ids = set()
    if user_id < 2e9:  # not a chat
        user_ids.add(user_id)
    for item_ in messages['items']:
        if not item_['from_id'] in user_ids:
            user_ids.add(item_['from_id'])

        for f in item_.get('fwd_messages', []):
            if not f['user_id'] in user_ids:
                user_ids.add(f['user_id'])
    values = {
        'user_ids': ','.join(str(i) for i in user_ids if user_id > 0),
        'fields': 'photo_50'
    }
    response = vk_session.method('users.get', values=values)
    time.sleep(1)
    users = dict()
    for id_avatar in response:
        users.update({str(id_avatar['id']): id_avatar})

    if user_id >= 2e9:  # a chat
        response = vk_session.method('messages.getChat', values={
            'chat_id': int(user_id - 2e9)
        })
        time.sleep(1)
        users.update({user_id: response})
    return users
