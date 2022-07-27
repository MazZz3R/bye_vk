#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from actions import \
    delete_messages, delete_wall, delete_fave, delete_albums, delete_videos, delete_profile, delete_docs, \
    quit_program
from core.sleep_inhibitors import get_sleep_inhibitor
from core.updater import check_update, print_welcome

action_list = [
    delete_messages, delete_wall, delete_fave, delete_albums, delete_videos,
    delete_profile, delete_docs,
    quit_program
]


def main():
    with get_sleep_inhibitor():
        #  check_update()
        print_welcome()

        while True:
            print("\nВыберите действие:")
            for action_id, action in enumerate(action_list):
                print(f"{action_id+1:2}. {action.__doc__}")
            need_action_id = int(input("> ")) - 1
            action_list[need_action_id]()


if __name__ == "__main__":
    main()
