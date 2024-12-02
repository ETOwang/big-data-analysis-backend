import os


class Config:
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY') or 'root'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///users.db'
    SQLALCHEMY_BINDS = {
       'papers': 'sqlite:///papers.db',  # 'sqlite:///papers.db
       'users':  'sqlite:///users.db'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
