"""
This module creates the Flask APP and then, defines and controls routes for GET and POST requests
"""

from api.config import *

from datetime import datetime
import json

from flask import Flask, request, redirect, url_for, abort, jsonify

from api.request_handler import handle_post_request
from model import __version__ as _model_version
from api import __version__ as api_version

app = Flask(__name__, template_folder='templates')

# Remove annoying Flask logs
# recommend to set log.ERROR if we want to run in cloud
log.getLogger('werkzeug').setLevel(log.INFO)


# GET method: although I used only POST method for prediction I just kept it as skeleton
@app.route('/<version>/<ml_model>', methods=['GET'])
def api_index(version, ml_model):
    if version == 'v1':
        if ml_model in ML_MODELS:
            if request.method == 'GET':
                response = (400, 'Current prediction of sklearn model handles only HTTP POST method.')
            else:
                response = (400, 'Unsupported HTTP Method.')

            log.info(response[1])
            abort(response[0], description=response[1])
        else:
            msg = 'INVALID MODEL TYPE: ' + ml_model
            log.info(msg)
            abort(400, description=msg)
    else:
        return redirect(url_for('welcome', version=version))


# POST method: Use to predict the forecasted number of calls and staffs
# accepts payload data only in json format
@app.route('/<version>/<model_name>', methods=['POST'])
def sklearn_model_prediction(version, model_name):
    if version == 'v1':
        if model_name in ML_MODELS:
            request_time = datetime.now()
            if request.method == 'POST':
                response = handle_post_request(app.config['ml_model'], model_name, payload_data=request.json)
            else:
                response = (400, 'Unsupported HTTP Method.')

            response_time = datetime.now()
            if response[0] == 200:
                result = json.dumps(response[1])
                log.debug('Query took {} (hr:min:sec:ms/1000) time to get responded.'
                          .format(response_time - request_time))
                return result
            else:
                log.info(response[1])
                abort(response[0], description=response[1])
        else:
            msg = 'INVALID MODEL TYPE: ' + model_name
            log.info(msg)
            abort(400, description=msg)
    else:
        return redirect(url_for('welcome', version=version))


@app.route('/<version>/config', methods=['GET', 'POST'])
def config_index(version):
    if request.method == 'GET':
        if version == 'v1':
            return "v1 config connected - GET!"
        else:
            return redirect(url_for('welcome', version=version))
    elif request.method == 'POST':
        if version == 'v1':
            return "v1 config connected - POST!"
        else:
            return redirect(url_for('welcome', version=version))


@app.route('/health', methods=['GET'])
def health():
    if request.method == 'GET':
        return "Yes! I am still alive!"


@app.route('/version', methods=['GET'])
def version():
    if request.method == 'GET':
        return jsonify({'model_version': _model_version,
                        'api_version': api_version})


def start(ml_model):
    """
    kickoff function to run the app locally.
    :param ml_model: sklearn trained model
    :return: None
    """
    app.config['ml_model'] = ml_model

    # debug only works in main thread
    log.info('Starting...')
    app.run(host='127.0.0.1', port=5000, debug=False, load_dotenv=True)
