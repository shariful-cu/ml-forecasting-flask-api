import pytest
from api.server import app as flask_app
from model.pool_models import PoolModels

@pytest.fixture()
def ml_model():
    ml_model = PoolModels()
    ml_model.init_ml_models()
    return ml_model


@pytest.fixture()
def app(ml_model):
    flask_app.config['ml_model'] = ml_model
    yield flask_app


@pytest.fixture()
def test_client(app):
    return app.test_client()
