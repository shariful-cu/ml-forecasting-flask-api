"""
This module aims to set and get of the trained model and use it for prediction as well.
"""
from api.config import *

import pickle
import pandas as pd

from model.ml_model import Model


class SklearnModel(Model):
    def __init__(self, is_primary):
        Model.__init__(self, is_primary)
        # Guest users
        self.__sklearn_model = None

    def get_model(self):
        return self.__sklearn_model

    def set_model(self):
        model_loc = os.path.join(DATA_DIR, SKLEARN_MODEL_NAME)
        self.__sklearn_model = pickle.load(open(model_loc, 'rb'))

    def predict(self, test_df):
        loaded_model = self.get_model()
        if loaded_model:
            return loaded_model.predict(test_df)
        else:
            return None

    @staticmethod
    def load_csv_data(path):
        return pd.read_csv(path)


if __name__ == '__main__':
    # mock test data sample
    test_instance = {
        "max_wind": 7.0,
        "min_temp": 65.62399999999985,
        "max_temp": 90.65959999999984,
        "weather": "sky is clear",
        "prev_week": 3587.0,
        "day_of_week": 6.0
    }

    model = SklearnModel(True)
    model.set_model()

    aa = model.predict(pd.DataFrame(test_instance, index=[0]))[0]

    print(f'test input: {test_instance}')
    print(f'predicted output: {model.predict(pd.DataFrame(test_instance, index=[0]))}')

