import logging as log
from datetime import datetime
import os
import pathlib

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent.parent

SKLEARN_MODEL_NAME = '311_pipeline.pkl'
ML_MODELS = ['sklearn']

DATA_DIR = os.path.join(PACKAGE_ROOT, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# mainly depends on the num of metrics and doubles it for safe,
# assuming generating and writing matrices takes (much) longer time than reading and refreshing them in the app
RELOAD_SIGNAL_PIPELINE_SIZE = 5

# depends on (hike of the reading number) * (maximum time of a reading)
SWAPPING_PATIENCE_PERIOD = 10

# level usage guideline:
# DEBUG: for DEVELOPMENT only
# INFO: an execution is worth to notice, for developers to know the program running PROGRESS
# WARNING: the program is running in RISK and needs attention
# ERROR: an error occurs in the program and needs IMMEDIATE attention
# CRITICAL: a FATAL error occurs and the program will shut down immediately
log.basicConfig(format='%(asctime)s - %(levelname)s - %(module)s - %(message)s', level=log.INFO)

# make a balance between polling workload and real time requirement
RELOAD_POLLING_INTERVAL = 10  # adjust based on the running environment

# make a balance between CPU workload and real time requirement
RELOAD_TICKING_INTERVAL = 5  # adjust based on the running environment

# for API to wait for ml models availability
API_NAPPING_TIME = 10
API_PATIENCE = 6


def check_local_repository(path):
    if os.path.exists(path):
        return True
    else:
        log.error('Local data repository does not exist!')
        return False


def sys_init(ml_model):
    """
    Initialization (check data repository, load model) before running the app
    """
    if not check_local_repository(DATA_DIR):
        log.error('Repository checking failed!')
        return False

    if not load_ml_models(ml_model):
        log.error('FAILED loading model!')
        return False

    return True


def load_ml_models(ml_model):
    try:
        ml_model.init_ml_models()
    except FileNotFoundError:
        return False

    return True


def get_local_file_last_modified(path):
    """
    :param path: file name
    :return: last modification timestamp of that file
    """
    modification_time_since_epoch = os.path.getmtime(path)
    return datetime.utcfromtimestamp(modification_time_since_epoch)

