from lib import config

def main():
    config_data = config.import_config_data()
    print(config_data.folder_cfg_file)

    all_folders = config.read_folder_config(config_data)

    for row in all_folders:
        print(row)

if __name__ == "__main__":
    main()
    