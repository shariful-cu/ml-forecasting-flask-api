from api.config import PACKAGE_ROOT
import os

MODEL_VERSION_PATH = os.path.join(PACKAGE_ROOT, 'model', 'VERSION.txt')

with open(MODEL_VERSION_PATH, 'r') as version_file:
    __version__ = version_file.read().strip()
