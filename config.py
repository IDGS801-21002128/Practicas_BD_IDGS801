import os
from sqlalchemy import create_engine

import urllib

class Config(object):
    SECRET_KEY = "Clave secreta"
    SESSION_COOKIE_SECURE=False

class DevelomentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:1234@127.0.0.1/bdiddgs801"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
