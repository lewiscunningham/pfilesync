from lib import config, file_processing, logger
import logging

def backup():
    config_data = config.import_config_data()

    logger.loginit(config_data)

    logging.info(f"Logging for PFileSync")
    logging.info(f"Configured using file: {config_data.folder_cfg_file}")

    all_folders = config.read_folder_config(config_data)

    for row in all_folders:
        file_processing.process_folder(row)

if __name__ == "__main__":
    backup()
    