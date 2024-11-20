
"""Django's command-line utility for administrative tasks."""
import os
import sys
import pathlib

THIS_FILE_PATH = pathlib.Path(__file__).resolve() # file path
NBS_DIR = THIS_FILE_PATH.parent
REPO_DIR = NBS_DIR.parent
DJANGO_BASE_DIR = REPO_DIR / "src"
DJANGO_PROJECT_SETTINGS_NAME = 'cfehome'

def init_django():
    """Run administrative tasks."""
    os.chdir(DJANGO_BASE_DIR) # root directory of project we will be working on
    sys.path.insert(0, str(DJANGO_BASE_DIR))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfehome.settings')
    os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
    import django
    django.setup()