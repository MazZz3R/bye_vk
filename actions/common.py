#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

from core.download import escape
from core.path_helper import data_path

YES_CHAR = '+'
YES_NO_PROMPT = '(введите "' + YES_CHAR + '" для продолжения)> '
ARE_YOU_SURE = 'Вы уверены?\n' + YES_NO_PROMPT
ARE_YOU_DEFINITELY_SURE = 'Вы точно уверены? Действие нельзя отменить\n' \
                          + YES_NO_PROMPT

FAVE_TYPES = ['Photos', 'Posts', 'Videos', 'Users', 'Links', 'MarketItems']


def are_you_sure() -> bool:
    sure = input(ARE_YOU_SURE)
    if sure != YES_CHAR:
        return False

    sure = input(ARE_YOU_DEFINITELY_SURE)
    if sure != YES_CHAR:
        return False
    return True


def print_owner_info(owner):
    print('Полное имя: {} {} [id: {}]'.format(
        owner['first_name'], owner['last_name'], owner['id']))


def get_user_dump_dir(owner) -> str:
    return os.path.join(
        data_path('dumps'),
        escape(f'{owner["first_name"]} {owner["last_name"]} [{owner["id"]}]')
    )


def pluralize(number: int, single: str, few: str, many: str) -> str:
    n = abs(number)
    n %= 100
    if 5 <= n <= 20:
        return many

    n %= 10
    if n == 1:
        return single
    if 2 <= n <= 4:
        return few
    return many


def append_to_json(json_path: str, vk_collection, id_key: str):
    saved_collection = {
        'count': 0,
        'items': []
    }
    if os.path.exists(json_path) and os.path.isfile(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            saved_collection = json.load(f)

    id_to_item = dict()
    for item in saved_collection['items']:
        id_to_item[item[id_key]] = item

    for item in vk_collection['items']:
        id_to_item[item[id_key]] = item

    saved_collection['count'] = len(id_to_item)
    saved_collection['items'] = list(id_to_item.values())

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(saved_collection, f, separators=(',', ':'), ensure_ascii=False)
    return saved_collection


def print_messages_api_deprecated():
    print('Ошибка! Невозможно получить доступ к сообщениям\n'
          'К сожалению, с 15 февраля 2019 API vk.com закрыл доступ на чтение сообщений для приложений, '
          'не прошедших верификацию.\n'
          'Официальный анонс: https://vk.com/dev/messages_api\n'
          'Разъяснение, что приложение не должно содержать автоматизацию пользовательских действий '
          '(увы, наш случай) https://vk.com/wall-1_390510\n'
          'Присоединиться к негодующим можно здесь https://vk.com/wall-1_389441\n')
    input('Нажмите Enter, чтобы выразить свою досаду и продолжить\n')
