import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-secret-key'
    DISPLAY_CMD = True
