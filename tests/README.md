# Automated Tests of NYC311 Call Forecasting APIs

### Structure of test suit:
```
├── ../conftest.py   
├── ../functional/test_endpoints.py                          <-- endpoints test cases under this class
│   ├── test_health_endpoint_returns_200()
│   ├── test_version_endpoint_returns_version()
│   ├── test_prediction_endpoint_with_valid_input_data()
├── ../functional/test_validation.py                          <-- test validation of input data
│   ├── test_prediction_endpoint_with_invalid_min_temp()
│   ├── test_prediction_endpoint_with_invalid_max_temp()
├── ../unit/test_model.py                          <-- test validation of input data
│   ├── test_sklearn_model_setting_and_loading()
│   ├── test_sklearn_model_prediction_on_test_data_sample()
```     
### Local Testing
Go test suit directory `(../tests/)`

Command for testing all test cases
```
python -m pytest -v
```
Command for testing a single test case
```
pytest test_endpoints.py::TestEndpoints::test_prediction_endpoint_with_valid_input_data
```
Command for testing with printing log messages in console
```
 pytest -s test_validation.py::TestDataValidation::test_prediction_endpoint_with_invalid_max_temp
```

Command for testing a group of test cases defined with `mark` statement(see in`pytest.ini`). 

For example, test a group of test cases marked by `test_data_validation` as:
```
pytest -v -m test_data_validation
```