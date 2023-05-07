from flask import request, jsonify, Blueprint, abort
from config.database import User, user_schema
from config.database import db
from email_validator import validate_email, EmailNotValidError
from services.auth import extract_auth_token, decode_token
import jwt


users = Blueprint('users', __name__, url_prefix='/user')


# Define the user routes

# The user sends a POST request to the /user route with a JSON body containing the user_name, password and email.
# The server responds with the user object.

@users.route('/', methods=['POST'], strict_slashes=False)
def signup():

    errors = {}

    if ('user_name' not in request.json):
        errors['user_name'] = 'string is missing'
    elif type(request.json['user_name']) != str:
        errors['user_name'] = 'must be a string'

    if ('password' not in request.json):
        errors['password'] = 'string is missing'
    elif type(request.json['password']) != str:
        errors['password'] = 'must be a string'

    if ('email' not in request.json):
        errors['email'] = 'string is missing'
    elif type(request.json['email']) != str:
        errors['email'] = 'must be a string'
    else:
        try:
            validate_email(request.json['email'])
        except EmailNotValidError as e:
            errors['email'] = str(e)

    if (len(errors) != 0):
        return jsonify(errors), 400

    user_name = request.json['user_name']
    password = request.json['password']
    email = request.json['email']

    userWithTheSameUsername = User.query.filter_by(user_name=user_name).first()
    if userWithTheSameUsername:
        return {'username': f'username {user_name} is taken'}, 409

    userWithTheSameEmail = User.query.filter_by(email=email).first()
    if userWithTheSameEmail:
        return {'email': f'email {email} is taken'}, 409

    user = User(user_name=user_name, password=password, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify(user_schema.dump(user)), 201


# The user sends a GET request to the /user route
# The server responds with the user object.

@users.route('/', methods=['GET'], strict_slashes=False)
def get_user_info():

    auth_token = extract_auth_token(request)
    user_id = None
    if auth_token:
        try:
            user_id = decode_token(auth_token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            abort(401)
    else:
        return jsonify({"auth_token": "No token was provided"}), 401

    user = User.query.filter_by(id=user_id).first()

    if (not user):
        return jsonify({"user": f"User with id {user_id} found"}), 404

    return jsonify(user_schema.dump(user)), 200
