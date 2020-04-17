#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from actions.common import print_messages_api_deprecated

try:
    import simplejson as json
except ImportError:
    import json


def dump_messages(only_first=False):
    """Выгрузить сообщения [устарел]"""
    print_messages_api_deprecated()
