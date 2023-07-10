"""
This is the main or starting module to run the NYC311 Call Forcasting APIs
"""

from api.config import *

import sys
import time
from threading import Thread

from model.pool_models import PoolModels
from model_reloader import reloader
from api import server


def main():
    log.debug('Running in development mode and locally.')

    log.info('Initializing the system...')

    watch_dog = 0
    while True:
        ml_model = PoolModels()
        if not sys_init(ml_model):
            log.error('Initialization failed! Wait and try periodically ...')
            time.sleep(API_NAPPING_TIME)
            watch_dog += 1
        else:
            break
        if watch_dog == API_PATIENCE:
            log.critical('API is out of patience. Existing the system!')
            sys.exit()

    # run producer and consumer in two different threads
    # consumer - always serve the latest ML MODEL
    # producer - refresh the current ML MODEL if a new version is uploaded
    reloader.start(ml_model)

    time.sleep(1)

    # kickoff flask app as a separate thread (a daemon will exit when main ends)
    Thread(target=server.start, args=(ml_model,), daemon=False).start()


if __name__ == '__main__':
    main()
