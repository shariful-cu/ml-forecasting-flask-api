"""
This module aims to reload the trained model when it will be refreshed with the newer trained model
"""
from api.config import *

from queue import Queue
from threading import Thread

from model_reloader import reload_signal_consumer, reload_signal_producer


def start(trained_model):
    pipeline = Queue(maxsize=RELOAD_SIGNAL_PIPELINE_SIZE)

    log.info('Starting reload signal producer...')
    Thread(target=reload_signal_producer.start, args=(pipeline,), daemon=True).start()

    log.info('Starting reload signal consumer...')
    Thread(target=reload_signal_consumer.start, args=(trained_model, pipeline,), daemon=True).start()
