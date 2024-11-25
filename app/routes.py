from flask import Flask
from .config import Config
from .models import db
from .api.paper import search_papers

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化数据库
    db.init_app(app)

    # 注册 API 路由
    app.register_blueprint(search_papers, url_prefix='/api')

    return app

