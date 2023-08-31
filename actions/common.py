#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

from core.path_helper import data_path

YES_CHAR = "+"
YES_NO_PROMPT = "(введите \"" + YES_CHAR + "\" для продолжения)> "
ARE_YOU_SURE = "Вы уверены?\n" + YES_NO_PROMPT
ARE_YOU_DEFINITELY_SURE = "Вы точно уверены? Действие нельзя отменить\n" \
                          + YES_NO_PROMPT

FAVE_TYPES = ["Photos", "Posts", "Videos", "Users", "Links", "MarketItems"]


def are_you_sure() -> bool:
    sure = input(ARE_YOU_SURE)
    if sure != YES_CHAR:
        return False

    sure = input(ARE_YOU_DEFINITELY_SURE)
    return sure == YES_CHAR


def print_owner_info(owner):
    print(f"Полное имя: {owner['first_name']} {owner['last_name']} [id: {owner['id']}]")


def pluralize(number: int, single: str, few: str, many: str) -> str:
    n = abs(number)
    n %= 100
    if 5 <= n <= 20:
        return many

    n %= 10
    if n == 1:
        return single
    return few if 2 <= n <= 4 else many
