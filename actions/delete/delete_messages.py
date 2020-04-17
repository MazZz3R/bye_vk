#!/usr/bin/python3
# -*- coding: utf-8 -*-

from actions.common import print_messages_api_deprecated

try:
    import simplejson as json
except ImportError:
    import json


def delete_messages():
    """Удалить все диалоги [устарел]"""
    print_messages_api_deprecated()
