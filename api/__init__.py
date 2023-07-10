from api.config import PACKAGE_ROOT
import os

API_VERSION_PATH = os.path.join(PACKAGE_ROOT, 'VERSION.txt')

with open(API_VERSION_PATH, 'r') as version_file:
    __version__ = version_file.read().strip()
