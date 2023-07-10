"""
This module defines the generic Model class interface that will be inherited by any trained model class
with the two mandatory get_model() and set_model() methods.
"""

from abc import ABC, abstractmethod
from threading import Lock


class Model(ABC):

    def __init__(self, is_primary):
        self.__primary = is_primary
        self._lock = Lock()

    def is_primary(self):
        return self.__primary

    def set_primary(self, is_primary):
        with self._lock:
            self.__primary = is_primary

    @abstractmethod
    def get_model(self):
        pass

    @abstractmethod
    def set_model(self):
        pass
