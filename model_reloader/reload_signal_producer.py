"""
pool the latest sklearn model if the existing one is updated
"""
import os.path

from api.config import *
import time
from datetime import datetime


def start(pipeline):
    timestamps = dict()

    initialize_timestamp(timestamps, SKLEARN_MODEL_NAME, DATA_DIR)

    while True:
        time.sleep(RELOAD_POLLING_INTERVAL)

        log.debug('Polling')

        # note that all comparisons are based on timezone.utc
        if not pipeline.full():
            check_timestamp(pipeline, timestamps, SKLEARN_MODEL_NAME, DATA_DIR)
        else:
            log.warning('The queue is full. Wait for all proceeded and current reload request is discarded!')
            pipeline.join()  # block the main thread until the queue is empty


def initialize_timestamp(timestamps, file_name, data_dir):
    try:
        timestamps[file_name] = get_local_file_last_modified(os.path.join(data_dir, file_name))
    except FileNotFoundError:
        log.warning('Timestamp for {} cannot be initialized! Set it to 1970/01/01 00:00:00.'.format(file_name))
        timestamps[file_name] = datetime.utcfromtimestamp(0)


def check_timestamp(pipeline, timestamps, file_name, data_dir):
    timestamp = None
    try:
        timestamp = get_local_file_last_modified(os.path.join(data_dir, file_name))
    except FileNotFoundError:
        log.warning('File {} does not exist!'.format(file_name))

    if timestamp is not None and timestamp > timestamps[file_name]:
        log.info('Reload request found: {0}, old: {1}, new: {2}'.format(file_name, timestamps[file_name], timestamp))
        timestamps[file_name] = timestamp
        pipeline.put(file_name)
        log.info('Reload requests have: {}'.format(pipeline.qsize()))
