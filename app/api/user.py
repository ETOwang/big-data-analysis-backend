from flask import request, jsonify, Blueprint
from werkzeug.exceptions import BadRequest
from flask_jwt_extended import create_access_token

from app.models import User  # Assuming User model is already defined
from app import db, bcrypt  # Assuming db and bcrypt are already initialized

auth = Blueprint('auth', __name__)


@auth.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate input data
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        raise BadRequest("Missing required fields")

    username = data['username']
    email = data['email']
    password = data['password']

    # Check if email already exists
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"status": "error", "message": "Email already in use"}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create new user and save to DB
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"status": "success", "message": "Registration successful"}), 0


@auth.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    email = data['email']
    password = data['password']

    # Fetch user by email
    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"status": "error", "message": "Invalid email or password"}), 400

    # Create JWT token
    access_token = create_access_token(identity=user.email)
    return jsonify({"status": "success", "token": access_token})
