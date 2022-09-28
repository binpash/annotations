import json
# import os
import pkgutil

# from pash_annotations.config.definitions import ROOT_DIR

def get_json_data(cmd_name):
    command_json_fn = f'{cmd_name}.json'
    # get man page data for command as dict
    # command_json_fn_absolute: str = os.path.join(ROOT_DIR, 'pash_annotations/command_flag_option_info/data', command_json_fn)
    command_json_fn_absolute: str = "command_flag_option_info/data" + command_json_fn
    try:
    #     with open(command_json_fn_absolute) as f:
    #         json_data = json.load(f)
        pkgutil.get_data(__name__, command_json_fn_absolute)
    # except FileNotFoundError:
    except Exception:
        try:
    #         command_json_fn_absolute: str = os.path.join(ROOT_DIR, 'pash_annotations/command_flag_option_info/data/_default_data_for_commands.json')
            command_json_fn_absolute: str = "command_flag_option_info/data/_default_data_for_commands.json"
            with open(command_json_fn_absolute) as f:
                json_data = json.load(f)
        # except FileNotFoundError:
        except Exception:
            raise Exception(f'json-File for default values not found.')
    return json_data

