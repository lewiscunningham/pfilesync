from dataclasses import dataclass
from pathlib import Path
import configparser
import csv
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

    config.read('config/pfilesync.cfg')

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

                
if __name__ == "__main__":
    import_config_data()
    