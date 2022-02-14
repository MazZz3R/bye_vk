#!/usr/bin/python3
# -*- coding: utf-8 -*-
import webbrowser


def delete_profile():
    """Удалить страницу вк"""
    webbrowser.open("https://vk.com/settings?act=deactivate")
