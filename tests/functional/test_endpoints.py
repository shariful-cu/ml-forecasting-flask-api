import json
from datetime import date
import pytest

from model import __version__ as _model_version
from api import __version__ as api_version


class TestEndpoints:
    @pytest.mark.test_endpoints
    def test_health_endpoint_returns_200(self, test_client):
        """
        GIVEN a Flask application for testing
        WHEN health check endpoint '/health' is requested (GET)
        THEN check health status is OK (200)
        """
        response = test_client.get('/health')
        assert response.status_code == 200

    @pytest.mark.test_endpoints
    def test_version_endpoint_returns_version(self, test_client):
        """
        GIVEN a Flask application for testing
        WHEN version endpoint '/version' is requested (GET)
        THEN check version status and current active versions of API and ML Model
        """
        response = test_client.get('/version')
        assert response.status_code == 200
        response_json = json.loads(response.data)
        assert response_json['model_version'] == _model_version
        assert response_json['api_version'] == api_version

    @pytest.mark.test_endpoints
    def test_config_endpoint_return_connected_version_info(self, test_client):
        """
        GIVEN a Flask application for testing
        WHEN config endpoint '/v1/config' is requested (GET or POST)
        THEN Just provide a message if v1 API is configured and connected
        """
        response = test_client.get('/v1/config')
        assert response.status_code == 200

    @pytest.mark.test_endpoints
    def test_prediction_endpoint_with_valid_input_data(self, test_client):
        """
        GIVEN a Flask application, a valid forecasting input data (json format), and the expected output
        WHEN Prediction endpoint '/v1/sklearn' is requested (POST) with the given valid input data
        THEN check prediction status is OK (200) and forcasting values are matched with the expected one
        """

        input_data = {
            "max_wind": 7.0,
            "min_temp": 65.62399999999985,
            "max_temp": 90.65959999999984,
            "weather": "sky is clear",
            "prev_week": 3587.0,
            "day_of_week": 6.0
        }

        forecasted_output = {
            'forecast_date': str(date.today()),
            'num_calls_forecasted': 3648,
            'num_staff_forecasted': 9
        }

        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }

        response = test_client.post('/v1/sklearn', data=json.dumps(input_data), headers=headers)

        assert response.status_code == 200

        response_json = json.loads(response.data)

        assert response_json['forecast_date'] == forecasted_output['forecast_date']
        assert response_json['num_calls_forecasted'] == forecasted_output['num_calls_forecasted']
        assert response_json['num_staff_forecasted'] == forecasted_output['num_staff_forecasted']
