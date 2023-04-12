from flask import Flask, request, jsonify, abort, Blueprint
from config.bcrypt import bcrypt
from services.auth import create_token
from models.user import User

authentication = Blueprint('authentication', __name__, url_prefix='/authentication')


@authentication.route('/', methods=['POST'])
def authenticate():

    errors = {}

    if('user_name' not in request.json) :
        errors['user_name'] = 'string is missing'
    elif type(request.json['user_name']) != str:
        errors['user_name'] = 'must be a string'

    if('password' not in request.json):
        errors['password'] = 'string is missing'
    elif type(request.json['password']) != str:
        errors['password'] = 'must be a string'

    if(len(errors) != 0):
        return jsonify(errors), 400

    user_name = request.json['user_name']
    password = request.json['password']

    user = User.query.filter_by(user_name = user_name).first()

    if not user or not bcrypt.check_password_hash(user.hashed_password, password):
        abort(401)

    return {"token": create_token(user.id)}, 200

