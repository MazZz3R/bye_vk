#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
