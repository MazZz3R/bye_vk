#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time

import vk_api


def on_error_retry(func):
    def func_wrapper(*args, **kwargs):
        timeouts = [5, 10, 15, 30]

        while True:
            try:
                return func(*args, **kwargs)
            except IOError as ex:
                sys.stderr.write(str(ex) + '\n')
                timeout = timeouts.pop(0) if len(timeouts) > 1 else timeouts[0]
                sys.stderr.write('Sleeping ' + str(timeout) + ' seconds and retrying\n')
                time.sleep(timeout)
    return func_wrapper


class VkToolsWithRetry(vk_api.VkTools):
    @on_error_retry
    def get_all(self, *args, **kwargs):
        return super().get_all(*args, **kwargs)


class VkApiWithRetry(vk_api.VkApi):
    @on_error_retry
    def method(self, *args, **kwargs):
        return super().method(*args, **kwargs)
