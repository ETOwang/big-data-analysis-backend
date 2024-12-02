from flask import request, jsonify, Blueprint
from flask_cors import cross_origin
from werkzeug.exceptions import BadRequest
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from app.models import User  # Assuming User model is already defined
from app import db, bcrypt  # Assuming db and bcrypt are already initialized

auth = Blueprint('auth', __name__)


@auth.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    print(data)
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

    return jsonify({"status": "success", "message": "Registration successful", "code": "000"}), 200


@auth.route('/api/auth/login', methods=['POST'])
def login():
    email = request.args.get('email')
    password = request.args.get('password')
    # Fetch user by email
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"status": "error", "message": "Invalid email or password"}), 400
    # Create JWT token
    access_token = create_access_token(identity=user.email)
    return jsonify({"status": "success", "token": access_token, "code": "000"}), 200


@auth.route('/api/users/profile', methods=['GET'])

def get_user_profile():
    # Get the identity of the current user
    current_user_email = "12@qq.com"
    print(current_user_email)
    # Fetch user by email
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    cur_role = user.role
    if user.role:
        user.role = "Normal"
    # Return user information
    user_info = {
        "username": user.username,
        "email": user.email,
        "role": cur_role
    }
    print(user_info)
    return jsonify({"status": "success", "data": user_info}), 200
