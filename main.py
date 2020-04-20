import os

from nbt import *


def print_uuid_info(path, islevel=False):
    file = nbt.NBTFile(path, 'rb')

    LOOKUPLIST = [
        'UUIDLeast',
        'UUIDMost',
        'XpLevel'
    ]

    print('Showing tags for ' + ('owner' if islevel else 'player:'))
    print(file.filename)
    # print(file.pretty_tree())
    for key in LOOKUPLIST:
        if islevel:
            tag = file['Data']['Player'][key]
        else:
            tag = file[key]
        print(tag.tag_info())
    print()


def swap_uuid(level_path, playerdata_path):
    level = nbt.NBTFile(level_path, 'rb')
    player = nbt.NBTFile(playerdata_path, 'rb')

    swaplist = ['UUIDMost', 'UUIDLeast', 'XpLevel']
    for key in swaplist:
        player_tag = player[key]
        owner_tag = level['Data']['Player'][key]
        print(f'old {key}: {owner_tag}')
        print(f'new {key}: {player_tag}')

        level['Data']['Player'][key] = player_tag

    player_tag = player
    owner_tag = level['Data']['Player']
    print(f'old : {owner_tag}')
    print(f'new : {player_tag}')
    level['Data']['Player'] = player_tag

    prompt(f'Save changes in {level_path}?', yes_callback=level.write_file)


def prompt(question, yes_callback=lambda: None, no_callback=lambda: None):
    while True:
        print(f'{question} (Y/n)')
        choice = input()
        if choice == 'Y':
            yes_callback()
            print('Done')
            return
        elif choice == 'n':
            no_callback()
            print('Aborted')
            return


def get_uuid(playername):
    db = {
        'tmpkd': '4a30e7b4-b4f4-3668-88ca-3a81ac81510b',
        'irusland': '2076ce78-c3cf-4a7e-8799-b6de177ed8b9',
        'unknown': '4650c991-8229-11ea-8e84-b42e996a7d7a',
        'irusland2': '2076ce78-c3cf-4a7e-8799-b6de177ed8b9 (2)'
    }
    try:
        return db[playername]
    except KeyError:
        message = f'Player "{playername}" not found'
        raise Exception(message)


def find_file(uuid, playerdata_dir):
    for filename in os.listdir(playerdata_dir):
        if filename.startswith(uuid):
            return filename


if __name__ == '__main__':
    print('World path:')
    WORLD_DIR = input()
    PLAYERDATA_DIR = os.path.join(WORLD_DIR, 'playerdata')
    LEVEL_FILE_PATH = os.path.join(WORLD_DIR, 'level.dat')
    LEVEL_OLD_FILE_PATH = os.path.join(WORLD_DIR, 'level.dat_old')

    # Before
    print_uuid_info(LEVEL_FILE_PATH, islevel=True)
    print_uuid_info(LEVEL_OLD_FILE_PATH, islevel=True)
    for dir, _, files in os.walk(PLAYERDATA_DIR):
        for file in files:
            print_uuid_info(os.path.join(dir, file))

    # Swap
    print('Type player name to change ownership:')
    PLAYER_NAME = input()
    uuid = get_uuid(PLAYER_NAME)
    uuid_file = find_file(uuid, PLAYERDATA_DIR)
    swap_uuid(LEVEL_FILE_PATH, os.path.join(PLAYERDATA_DIR, uuid_file))
    swap_uuid(LEVEL_OLD_FILE_PATH, os.path.join(PLAYERDATA_DIR, uuid_file))

    # After
    print_uuid_info(LEVEL_FILE_PATH, islevel=True)
    print_uuid_info(LEVEL_OLD_FILE_PATH, islevel=True)
    for dir, _, files in os.walk(PLAYERDATA_DIR):
        for file in files:
            print_uuid_info(os.path.join(dir, file))
