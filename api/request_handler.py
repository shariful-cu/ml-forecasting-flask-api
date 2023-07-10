"""
This module aims to handle requests from the end users
"""

from api.validation import validate_inputs
import pandas as pd
from datetime import date


def fahrenheit_to_kelvin(fahrenheit):
    return 273.5 + ((fahrenheit - 32.0) * (5.0/9.0))


def handle_sklearn_prediction_request(ml_model, payload_data):
    """
    Predict and compute the target forecasted number of calls and staff
    :param ml_model: sklearn model
    :param payload_data: json input
    :return: a dictionary of the response body
    """
    response_body = dict()
    min_temp_f = payload_data['min_temp']

    # convert fahrenheit to kelvin
    payload_data['min_temp'] = fahrenheit_to_kelvin(payload_data['min_temp'])
    payload_data['max_temp'] = fahrenheit_to_kelvin(payload_data['max_temp'])

    # load trained model and predict # of calls
    load_model = ml_model.load_sklearn_model()
    num_calls_forecasted = load_model.predict(pd.DataFrame(payload_data, index=[0]))[0]

    # calculate num of forecasted staff
    if min_temp_f < 25:
        num_staff_forecasted = num_calls_forecasted/600
    else:
        num_staff_forecasted = num_calls_forecasted/400

    # response
    response_body['forecast_date'] = str(date.today())
    response_body['num_calls_forecasted'] = int(num_calls_forecasted)
    response_body['num_staff_forecasted'] = int(num_staff_forecasted)

    return response_body


def handle_post_request(ml_model, model_name, payload_data=None):
    """
    Handle request by validating input data.
    Provide response with proper action based on the validation outcomes
    """

    # check input data validation
    if payload_data:
        error_msg = validate_inputs(payload_data)
        if error_msg:
            return 400, error_msg

    else:
        return 400, 'Missing mandatory json input data.'

    # handle ml models although this exercise has only one
    if model_name == 'sklearn':
        return 200, handle_sklearn_prediction_request(ml_model, payload_data)
    else:
        return 400, 'Unsupported machine learning model: {}'.format(model_name)


if __name__ == '__main__':
    # TODO: placeholder for unit testing
    print('Test different parameters and requests')

