"""
This module starts the consumer with the latest ml model as a separate python thread
"""

from api.config import *

import time


def start(ml_model, pipeline):
    while True:
        log.debug('Ticking')

        if not pipeline.empty():
            label = pipeline.get()
            log.info('Reload request received: {}'.format(label))
            log.info('Reload requests remain: {}'.format(pipeline.qsize()))
            ml_model.reload_ml_model(label)
            pipeline.task_done()  # decrease the counter, when zero, unlock 'join()'
        else:
            # to save some cpu resource, but note the (very low) risk of queue fullness
            time.sleep(RELOAD_TICKING_INTERVAL)
