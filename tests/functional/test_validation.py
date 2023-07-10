import json
import pytest


class TestDataValidation:
    @pytest.mark.test_data_validation
    def test_prediction_endpoint_with_invalid_min_temp(self, test_client):
        """
        GIVEN a Flask application and input data (json format) with an invalid forecasted minimum temperature
        WHEN Prediction endpoint '/v1/sklearn' is requested (POST) with the given invalid input data
        THEN check prediction status is 400
        """

        input_data = {
            "max_wind": 7.0,
            "min_temp": -20.62399999999985,
            "max_temp": 40.65959999999984,
            "weather": "sky is clear",
            "prev_week": 3587.0,
            "day_of_week": 6.0
        }
        expected = 400
        error_message = "min_temp must be greater than or equal to -20 degrees Fahrenheit!"

        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }

        response = test_client.post('/v1/sklearn', data=json.dumps(input_data), headers=headers)

        assert response.status_code == expected, error_message

    @pytest.mark.test_data_validation
    def test_prediction_endpoint_with_invalid_max_temp(self, test_client):
        """
        GIVEN a Flask application and input data (json format) with an invalid forecasted max temperature
        WHEN Prediction endpoint '/v1/sklearn' is requested (POST) with the given invalid input data
        THEN check prediction status is 400
        """

        input_data = {
            "max_wind": 7.0,
            "min_temp": 65.62399999999985,
            "max_temp": 115.65959999999984,
            "weather": "sky is clear",
            "prev_week": 3587.0,
            "day_of_week": 6.0
        }
        expected = 400
        error_message = "max_temp must be less than or equal to 115 degrees Fahrenheit!"

        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }

        response = test_client.post('/v1/sklearn', data=json.dumps(input_data), headers=headers)

        assert response.status_code == expected, error_message

