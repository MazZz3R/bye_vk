from actions import \
    dump_messages, dump_wall, dump_fave, dump_albums, dump_videos, \
    delete_messages, delete_wall, delete_fave, delete_albums, delete_videos, delete_profile, \
    render_to_html


def escape():
    """Выход"""
    exit(0)


action_list = [
    dump_messages, dump_wall, dump_fave, dump_albums, dump_videos,
    delete_messages, delete_wall, delete_fave, delete_albums, delete_videos,
    delete_profile, render_to_html,
    escape
]


def main():
    while True:
        print('\nВыберите действие:')
        for idx, action in enumerate(action_list):
            print('{0:2}. {1}'.format(idx + 1, action.__doc__))
        action_idx = int(input('> '))
        action_list[action_idx - 1]()


if __name__ == '__main__':
    main()
