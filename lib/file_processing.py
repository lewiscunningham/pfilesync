from pathlib import Path
from os import utime
from shutil import copyfile
import logging

def process_folder(config_row):
    input_folder = Path(config_row.get('input').strip())
    output_folder = Path(config_row.get('output').strip())
    glob = config_row.get('glob').strip()

    logging.info(f"Getting files from {input_folder} and moving them to {output_folder} where they match {glob}")

    for input in input_folder.glob('*.*'):
        file_name = input.name
        logging.info(f"Working on input {file_name}")
        file_size = input.stat().st_size
        last_access = input.stat().st_atime
        last_modification = input.stat().st_mtime

        output_file = output_folder.joinpath(file_name)
        out_file_size = 0
        out_last_modification = 0

        if output_file.exists():
            logging.info("File exists")
            out_file_size = output_file.stat().st_size
            out_last_modification = output_file.stat().st_mtime
        else:
            logging.info("File does not exist")

        if (file_size != out_file_size or last_modification != out_last_modification):
            logging.info("Copying file")
            copyfile(input, output_file)
            utime(output_file, (last_access, last_modification))
