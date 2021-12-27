from dataclasses import dataclass
from pathlib import Path
import configparser
import csv
from lib import logger

DEFAULT_CONFIG_FILE = 'config/pfilesync.cfg'

#import logging

@dataclass
class Configuration:
    config_location: Path
    folder_cfg_file: str
    log_level : int
    log_dir : Path
    log_name : str

def import_config_data():
    config = configparser.ConfigParser()

    if not Path(DEFAULT_CONFIG_FILE).is_file():
        logger.log_info("Config not found or not readable. Creating default.")
        create_raw_config()

    config.read(DEFAULT_CONFIG_FILE)

    config_file = config['default']['config']

    config_path = Path(config_file).absolute()

    config.read(f'{config_file}/pfilesync.cfg')

    folder_cfg_file = config['default']['folder_cfg']
    folder_config_path = Path(folder_cfg_file).absolute()

    log_level = config['default']['log_level']
    log_dir = config['default']['log_dir']
    log_path = Path(log_dir).absolute()
    log_name = config['default']['log_name']

    return Configuration(config_location=config_path, 
                         folder_cfg_file=folder_config_path, 
                         log_level=log_level, 
                         log_dir=log_path, 
                         log_name=log_name)

def read_folder_config(config : Configuration):
    with open(config.folder_cfg_file, newline='') as csvfile:
        fieldnames=['input', 'output', 'glob']
        csvreader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=',', quotechar='"')

        result_list = list(csvreader)

    return result_list


def create_raw_config():
    config = configparser.ConfigParser()
    config['default'] = {
                            'config':'./config',
                            'folder_cfg':'%(config)s/pfilesync_folders.cfg',
                            'log_level':0,
                            'log_dir':'config/log',
                            'log_name':'pfilesync_{dt}.log',
                        }
    with open(DEFAULT_CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

if __name__ == "__main__":
    import_config_data()
    