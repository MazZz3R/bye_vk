from actions import dump_messages, dump_wall, dump_fave, \
    delete_messages, delete_wall, \
    render_to_html, delete_fave, dump_albums


def escape():
    """Выход"""
    exit(0)


action_list = [
    dump_messages, dump_wall, dump_fave, dump_albums,
    delete_messages, delete_wall, delete_fave,
    render_to_html,
    escape
]


def main():
    while True:
        print('\nВыберите действие:')
        for idx, action in enumerate(action_list):
            print('{0}. {1}'.format(idx + 1, action.__doc__))
        action_idx = int(input('> '))
        action_list[action_idx - 1]()


if __name__ == '__main__':
    main()
