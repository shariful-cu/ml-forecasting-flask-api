import pytest
import pandas as pd

from model.sklearn_model import SklearnModel


class TestModel:
    @pytest.mark.test_model
    def test_sklearn_model_setting_and_loading(self, test_client):
        """
        GIVEN an instance of sklearn model class
        WHEN initialize the model
        THEN set and get a sklearn model
        """

        ml_model = SklearnModel(True)
        ml_model.set_model()
        load_model = ml_model.get_model()
        if load_model:
            expected = True
        else:
            expected = False

        assert expected is True

    @pytest.mark.test_model
    def test_sklearn_model_prediction_on_test_data_sample(self, test_client):
        """
        GIVEN an instance of sklearn model with a mock sample data and expected prediction value
        WHEN call the predict method
        THEN check prediction status is 400
        """

        # valid data sample
        test_instance = {
            "max_wind": 7.0,
            "min_temp": 65.62399999999985,
            "max_temp": 90.65959999999984,
            "weather": "sky is clear",
            "prev_week": 3587.0,
            "day_of_week": 6.0
        }
        expected = 7917.894555904091

        ml_model = SklearnModel(True)
        ml_model.set_model()
        load_model = ml_model.get_model()

        predicted = load_model.predict(pd.DataFrame(test_instance, index=[0]))[0]

        assert predicted == expected
