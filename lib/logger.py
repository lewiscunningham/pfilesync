import logging
import config
from datetime import date

def loginit(config_data ):
    logfiledir = config_data.log_dir

    logfilename = config_data.log_name

    today = date.today()

    template_values = {
        'dt': today.strftime("%Y%m%d"),
    }

    logfilename = logfilename.format(**template_values)

    log_complete = logfiledir.joinpath(logfilename)

    logging.basicConfig(filename=log_complete, encoding='utf-8', level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

