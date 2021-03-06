import json
import os
from config_new.definitions import ROOT_DIR

def get_json_data(cmd_name):
    command_json_fn = f'{cmd_name}.json'
    # get man page data for command as dict
    command_json_fn_absolute: str = os.path.join(ROOT_DIR, 'command_flag_option_info/data', command_json_fn)
    try:
        with open(command_json_fn_absolute) as f:
            json_data = json.load(f)
    except FileNotFoundError:
        raise Exception(f'File {command_json_fn_absolute} not found.')
    return json_data

