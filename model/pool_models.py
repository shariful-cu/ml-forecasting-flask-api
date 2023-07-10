"""
This module aims to load the latest trained model in two modes:
one is for consumer and the other is for producer.
The second one will be used to reload the model if a newer version is uploaded.
Consumer model will be refreshed if it is updated with the newer version of that model.
"""

import sys
import time

from model.sklearn_model import SklearnModel
from api.config import *


class PoolModels:
    def __init__(self):
        log.info('Initialized with the first sklearn model being set to primary/live/active')
        self.__sklearn_model_first = SklearnModel(True)
        self.__sklearn_model_second = SklearnModel(False)

    # refresh live model with the updated one
    def __update(self, active_model, inactive_model):
        # load newly updated model
        inactive_model.set_model()
        # just for safe
        time.sleep(1)
        # both True first
        inactive_model.set_primary(True)
        # now switch
        active_model.set_primary(False)
        # for ongoing readings to complete
        time.sleep(SWAPPING_PATIENCE_PERIOD)
        active_model.set_model()
        # just for safe
        time.sleep(1)

    # a complete load is supposed to be called only once in lunching the app
    def init_ml_models(self):
        log.info('Initializing ml models.')

        time.sleep(1)
        log.info('Loading sklearn model...')
        self.__sklearn_model_first.set_model()
        self.__sklearn_model_second.set_model()
        log.info('Sklearn model has been loaded successfully!')

    def reload_sklearn_model(self):
        log.info('Reloading sklearn model...')
        if self.__sklearn_model_first.is_primary():
            self.__update(self.__sklearn_model_first, self.__sklearn_model_second)
            log.info('Reloaded and activated the updated sklearn model.')
        elif self.__sklearn_model_second.is_primary():
            self.__update(self.__sklearn_model_second, self.__sklearn_model_first)
            log.info('Reloaded and activated the updated sklearn model.')
        else:
            log.critical('NO LIVE SKLEARN MODEL: Neither FIRST nor SECOND copy of sklearn model is set to live')
            sys.exit()

    def load_sklearn_model(self):
        if self.__sklearn_model_first.is_primary():
            return self.__sklearn_model_first.get_model()
        elif self.__sklearn_model_second.is_primary():
            return self.__sklearn_model_second.get_model()
        else:
            log.critical('NO LIVE SKLEARN MODEL: Neither FIRST nor SECOND copy of sklearn model is set to live')
            sys.exit()

    def reload_ml_model(self, model_name):
        if model_name == SKLEARN_MODEL_NAME:
            self.reload_sklearn_model()
        else:
            log.warning('NO RELOAD ML MODEL with the name {}'.format(model_name))
