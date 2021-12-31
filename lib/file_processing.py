from pathlib import Path
import os 
from shutil import copyfile
import logging
from lib import logger, config

def process_folder(config_row):
    logging.info(f"start process_folder - Config: {config_row}")
    input_folder = Path(config_row.get('input').strip())
    output_folder = Path(config_row.get('output').strip())
    glob = config_row.get('glob').strip()
    processed_row = {"source":input_folder,
                     "target":output_folder,
                     "filename":"",
                     "source_size":0,
                     "target_size":0,
                     "target_modify":0.0,
                     "source_modify":0.0,
                     "success":"",
                     "message":""
                     }

    files_processed = []

    if not output_folder.exists():  #check for folder instead of file? Not needed? output_folder.is_dir()
        logger.log_info(f"Creating folder: {output_folder}")
        output_folder.mkdir()

    #logging.info(f"Getting files from {input_folder} and moving them to {output_folder} where they match {glob}")

    globbed = (sorted(input_folder.glob(glob)))

    for input in sorted(input_folder.glob(glob)):
        try:
            file_name = input.name
            logger.log_info(f"Working on input {file_name}")
            processed_row["filename"] = file_name
            output_file = output_folder.joinpath(file_name)
            logger.log_info(f"output_file: {output_file}")

            if input.is_dir():
                root_dir = input.parents[0]

                child_dir = {
                    'input':str(input), 
                    'output':str(output_file), 
                    'glob':glob
                }
                process_folder(child_dir)
            else:
                root_dir = input

            logger.log_debug(f"input: {input} | Root Dir: {root_dir}")

            st_in = os.stat(input)
            logger.log_debug(f"os stat in: {st_in}")

            file_size = st_in.st_size
            last_access = st_in.st_atime
            last_modification = st_in.st_mtime

            processed_row["source_modify"] = last_modification
            processed_row["source_size"] = file_size

            out_file_size = 0
            out_last_modification = 0

            logger.log_debug(f"Check if output file exists: {output_file}")
            if output_file.exists():
                st_out = os.stat(output_file)
                logging.info(f"{output_file} File exists")
                out_file_size = st_out.st_size
                out_last_modification = st_out.st_mtime
            else:
                logger.log_debug("File does not exist")
                if output_file.is_dir():
                    output_file.mkdir()

            processed_row["target_modify"] = out_last_modification
            processed_row["target_size"] = out_file_size

            logger.log_debug("Check if output file input file")
            if (file_size != out_file_size or last_modification != out_last_modification):
                if not output_file.is_dir():
                    logger.log_debug("Copying file")
                    copyfile(input, output_file)
                    logger.log_debug("Setting time")
                    os.utime(output_file, (last_access, last_modification))
                processed_row["success"] = "success"
        except Exception as e:
            print(f"Error: {e}")
            logger.log_info(f"Error: {e}")
            processed_row["success"] = "failure"
            processed_row["message"] = e

        #logger.log_info(processed_row)
        files_processed.append(processed_row)
        logging.info(f"end process_folder - Config: {processed_row}")
    
    return files_processed
