import os
import json
from time import strftime, localtime
from datetime import datetime
from pathlib import Path


FOLDER = './files'
OUTPUT_FOLDER = 'output'
HISTORY_FILE = 'history.json'


def read_history():
    '''
    Reads from our history file to retrieve data.
    '''
    try:
        with open(HISTORY_FILE) as history_file:
            contents = history_file.read()
            data = json.loads(contents)
            return data

    # create the file if it doesn't exist and returns empty {}
    except FileNotFoundError:
        print('File {HISTORY_FILE} does not exist; creating it.')
        write_to_history()
        return read_history()


def write_to_history(data={}):
    '''
    Write data to our history file.
    '''
    with open(HISTORY_FILE, 'w') as f:
        json.dump(data, f)


def historicize(files):
    '''
    Adds a new entry to our history file with the renames we've just made, so
    we can easily revert them if needed.
    '''
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    history = read_history()
    history[now] = files
    write_to_history(history)



def move_file(old_path, new_path):
    '''
    Move a file from it old (current) path to a new path.
    '''
    print(f'Moving {old_path} to {new_path}.')
    try:
        os.rename(old_path, new_path)
    # when the subfolder doesn't exist, we create it and retry.
    except FileNotFoundError:
        new_folder = '/'.join(new_path.split('/')[:-1])
        create_folder(new_folder)
        move_file(old_path, new_path)


def create_folder(path):
    '''
    Creates a folder if not exists, else skip.
    '''
    Path(path).mkdir(parents=True, exist_ok=True)


def get_new_file_path(path, created_date):
    """
    Returns the 'clean' path of the file we want to tidy in a folder.
    """
    file_name = path.split('/')[-1]
    return f'{FOLDER}/{OUTPUT_FOLDER}/{created_date}/{file_name}'



def get_files(path='.', revert=False):
    '''
    For a directory and all it's subdirectories, get all files name and creation
    time.
    '''
    files = []

    if revert:
        history = read_history()
        keys = list(history.keys())
        if len(keys) == 0:
            print(f'No history available in {HISTORY_FILE}.')
            return []

        last_change = history.pop(keys[-1])
        # removes from the actual history of changes since we reverted
        write_to_history(history)

        return last_change


    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        # if the entry is a folder, then we re-run it on the folder to get all
        # its files
        if os.path.isdir(full_path):
            files.extend(get_files(full_path))

        else:
            files.append({
                "path": full_path,
                "new_path": get_new_file_path(
                    full_path,
                    strftime('%Y-%m-%d', localtime(os.stat(full_path).st_birthtime))
                )
            })

    historicize(files)

    return files



def rename(files, revert=False):
    '''
    Goes through all files we're passing it, and proceed with renaming.
    '''

    # we place files in an `output` folder at the root of current directory
    output = f'{FOLDER}/{OUTPUT_FOLDER}'
    create_folder(output)

    # for all creation dates, creates a folder and place all files in them.
    for file in files:
        if revert: move_file(file['new_path'], file['path'])
        else: move_file(file['path'], file['new_path'])

def run(revert=False):
    '''
    Our entry point!
    '''
    files = get_files(FOLDER, revert=revert)
    if len(files) > 0: rename(files, revert=revert)
    print('Done.')


run(revert=False)
