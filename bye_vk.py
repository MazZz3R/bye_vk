#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from actions import \
    demo, dump_messages, dump_wall, dump_fave, dump_albums, dump_videos, dump_docs, \
    delete_messages, delete_wall, delete_fave, delete_albums, delete_videos, delete_profile, \
    render_to_html, quit_program
from core.sleep_inhibitors import get_sleep_inhibitor
from core.stats import send_stats

action_list = [
    demo,
    dump_messages, dump_wall, dump_fave, dump_albums, dump_videos, dump_docs,
    delete_messages, delete_wall, delete_fave, delete_albums, delete_videos,
    delete_profile, render_to_html,
    quit_program
]


def main():
    with get_sleep_inhibitor():
        # Determine whether people use this application
        send_stats()

        while True:
            print('\nВыберите действие:')
            for idx, action in enumerate(action_list):
                print('{0:2}. {1}'.format(idx + 1, action.__doc__))
            action_idx = int(input('> '))
            action_list[action_idx - 1]()


if __name__ == '__main__':
    main()
