import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'root'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///papers.db'
    SQLALCHEMY_BINDS = {
        'users':  'sqlite:///users.db'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
