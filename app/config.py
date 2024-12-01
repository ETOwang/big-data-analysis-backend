import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'root'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{BASE_DIR}/instance/papers.db'
    # SQLALCHEMY_BINDS = {
    #     'users':  'sqlite:///instance/users.db'
    # }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
