from flask import request, jsonify, Blueprint
from config.database import User, user_schema
from config.database import db


users = Blueprint('users', __name__, url_prefix='/user')


@users.route('/', methods=['POST'])
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

    if (len(errors) != 0):
        return jsonify(errors), 400

    user_name = request.json['user_name']
    password = request.json['password']

    userWithTheSameUsername = User.query.filter_by(user_name=user_name).first()
    if userWithTheSameUsername:
        return {'error': f'username {user_name} is taken'}, 409

    user = User(user_name=user_name, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify(user_schema.dump(user)), 201
