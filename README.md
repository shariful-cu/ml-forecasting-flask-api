# ML Forcasting Flask APIs
### Overview

This Flask application provides the endpoint (http://127.0.0.1:5000/v1/sklearn) that can predict the number of calls expected based on the previous week’s calls and the weather forecast for the given day. An example of input data is (in json format):
```agsl
input_data = {
        "max_wind": 7.0,
        "min_temp": 65.62399999999985,
        "max_temp": 90.65959999999984,
        "weather": "sky is clear",
        "prev_week": 3587.0,
        "day_of_week": 6.0
    }
```

NB: I used [pytest](https://docs.pytest.org/en/stable/) for automatically testing its functionalities. See the another README file in ./tests/ 

## Installation Instructions
First download and open this submitted project named as 'nyc311-forecasting-api' using your convenient IDE (intelliJ, pycharm, etc.)

Create a new virtual environment (python 3.8):
```sh
$ cd nyc311-forecasting-api
$ python3 -m venv venv
```
Activate the virtual environment:
```sh
$ source venv/bin/activate
```
Install the python packages specified in requirements.txt:
```sh
(venv) $ pip install -r requirements.txt
```
### Download and upload the trained model in ./data/ directory
[trained sklearn model](https://acceleratorlake.blob.core.windows.net/code/311_pipeline.pkl)


### Run Application
Hit this command that will run the development server to serve the application at `host='127.0.0.1, port=5000`
```sh
(venv) $ python3 run.py
```
The server will be up on [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Testing

To run all the tests (see more detail instructions in README file located in `../tests/`:

```sh
(venv) $ python -m pytest -v
```

## EXAMPLE 
(first run the app then, test it using `curl` command)

REQUEST (POST)
```sh
$ curl -d '{"max_wind":7.0, "min_temp":65.62399999999985, "max_temp": 90.65959999999984, "weather": "sky is clear", "prev_week": 3587.0, "day_of_week": 6.0}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/v1/sklearn
```
RESPONSE (JSON):
```sh
{
  "forecast_date": "2023-07-08",
  "num_calls_forecasted": 3648,
  "num_staff_forecasted": 9
}
```

## WORKFLOWS
After hitting the run script (`run.py`):

1. App will be initialized by loading the trained sklearn model.
2. After initialization, it will run the producer and consumer in two different python threads.
3. Producer - refresh the current ML MODEL if a new version is uploaded in './data/'.
4. Consumer - always serve the latest ML MODEL.
5. Then, the Flask app will be started with a separate python thread.
6. App is now ready for handling your HTTP requests to predict the target forecasted number of calls and staff.

