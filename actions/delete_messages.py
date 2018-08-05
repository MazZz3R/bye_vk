#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.auth import get_session

try:
    import simplejson as json
except ImportError:
    import json

import vk_api


def delete_messages():
    """Удалить все диалоги"""

    vk_session = get_session()

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk_tools = vk_api.VkTools(vk_session)

    owner = vk_session.method('users.get')[0]
    print('Полное имя: {} {} [id: {}]'.format(owner['first_name'], owner['last_name'], owner['id']))

    first_time = True

    while True:
        print('Получаем диалоги...')
        dialogs = vk_tools.get_all(
            'messages.getConversations',
            max_count=200,
            values={'preview_length': '0'}
        )
        print('Количество диалогов:', dialogs['count'])

        if dialogs['count'] == 0:
            print("Все диалоги уже удалены!")
            return

        if first_time:
            sure = input('Вы уверены?\n(введите "y" или "д" для продолжения)> ')
            if sure.lower() not in ['y', 'д']:
                return

            sure = input('Вы точно уверены? Действие нельзя отменить\n(введите "y" или "д" для продолжения)> ')
            if sure.lower() not in ['y', 'д']:
                return

        for item in dialogs['items']:
            conversation = item['conversation']

            peer_id = conversation['peer']['id']
            peer_type = conversation['peer']['type']

            values = {'count': '10000'}

            if peer_type == 'user':
                values.update({'user_id': peer_id})
            elif peer_type == 'chat':  # FIXME test me
                values.update({'peer_id': conversation['peer']['local_id']})
            elif peer_type == 'group':  # FIXME test me
                values.update({'peer_id': conversation['peer']['local_id']})
            elif peer_type == 'email':  # FIXME test me
                values.update({'peer_id': conversation['peer']['local_id']})

            print('Удаляем %s...' % values)

            vk_session.method('messages.deleteConversation', values=values)

        again = input(
            'За один раз из каждого диалога можно удалить максимум 10000 сообщений.\n'
            'Попробовать удалить диалоги ещё раз?\n'
            '(введите "y" или "д" для продолжения)> ')
        if again.lower() not in ['y', 'д']:
            return
