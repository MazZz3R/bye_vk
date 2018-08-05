YES_NO_PROMPT = '(введите "y" или "д" для продолжения)> '
ARE_YOU_SURE = 'Вы уверены?\n' + YES_NO_PROMPT
ARE_YOU_DEFINITELY_SURE = 'Вы точно уверены? Действие нельзя отменить\n' \
                          + YES_NO_PROMPT

FAVE_TYPES = ['Photos', 'Posts', 'Videos', 'Users', 'Links', 'MarketItems']


def are_you_sure() -> bool:
    sure = input(ARE_YOU_SURE)
    if sure.lower() not in ['y', 'д']:
        return False

    sure = input(ARE_YOU_DEFINITELY_SURE)
    if sure.lower() not in ['y', 'д']:
        return False
    return True


def print_owner_info(owner):
    print('Полное имя: {} {} [id: {}]'.format(
        owner['first_name'], owner['last_name'], owner['id']))
