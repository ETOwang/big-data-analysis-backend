from flask import Flask
from .config import Config
from .models import db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
    # Initialize Bcrypt
    bcrypt.init_app(app)

    # Initialize JWT
    app.config['JWT_SECRET_KEY'] = 'root'  # 你的密钥
    jwt.init_app(app)

    # Initialize database
    db.init_app(app)
    # Enable CORS

    # Register blueprints
    from .api.user import auth as auth_blueprint
    from .api.paper import search_papers as search_papers_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(search_papers_blueprint)
    return app
