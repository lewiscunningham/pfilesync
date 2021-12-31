import logging
import config
from datetime import date

def loginit(config_data):
    logfiledir = config_data.log_dir

    if not logfiledir.exists():
        logfiledir.mkdir(parents=True, exist_ok=True)

    logfilename = config_data.log_name

    today = date.today()

    template_values = {
        'dt': today.strftime("%Y%m%d"),
    }

    logfilename = logfilename.format(**template_values)

    log_complete = logfiledir.joinpath(logfilename)

    logging.basicConfig(filename=log_complete, encoding='utf-8', level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    log = logging.getLogger("app_logger")

    return log


def log_info(msg):
    logging.info(msg)

def log_debug(msg):
    logging.debug(msg)

    
def close_log(log):
    x = logging._handlers.copy()
    for i in x:
        log.removeHandler(i)
        i.flush()
        i.close()    
