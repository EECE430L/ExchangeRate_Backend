from flask import Blueprint, request, jsonify, abort
from config.database import db
from config.database import Transaction, transaction_schema, transactions_schema
from config.database import User
from services.auth import extract_auth_token, decode_token
import jwt


transactions = Blueprint('transactions', __name__, url_prefix='/transaction')


@transactions.route('/', methods=['POST'], strict_slashes=False)
def create_transaction():

    errors = {}
    second_party = "Third Party"

    if ('usd_amount' not in request.json):
        errors['usd_amount'] = 'float is missing'
    elif (type(request.json['usd_amount']) != int and type(request.json['usd_amount']) != float):
        errors['usd_amount'] = 'must be an integer or a float'

    if ('lbp_amount' not in request.json):
        errors['lbp_amount'] = 'float is missing'
    elif (type(request.json['lbp_amount']) != int and type(request.json['lbp_amount']) != float):
        errors['lbp_amount'] = 'must be an integer or a float'

    if ('usd_to_lbp' not in request.json):
        errors['usd_to_lbp'] = 'boolean is missing'
    elif (type(request.json['usd_to_lbp']) != bool):
        errors['usd_to_lbp'] = 'must be a boolean'

    if ('receiver' in request.json and type(request.json['receiver']) != str):
        errors['receiver'] = 'must be a string'

    if (len(errors) != 0):
        return jsonify(errors), 400

    usd_amount = request.json['usd_amount']
    lbp_amount = request.json['lbp_amount']
    usd_to_lbp = request.json['usd_to_lbp']

    auth_token = extract_auth_token(request)
    user_id = None
    if auth_token:
        try:
            user_id = decode_token(auth_token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            abort(401)

    if ('second_party' in request.json):
        second_party = request.json['second_party']
        SecondParty = User.query.filter_by(
            user_name=second_party).first()
        if (not SecondParty):
            return jsonify({"receiver": f"A user with username {second_party} was not found"}), 404
        elif (SecondParty.id == user_id):
            return jsonify({"receiver": "You cannot send money to yourself"}), 400

    transaction = Transaction(
        usd_amount=usd_amount, lbp_amount=lbp_amount, usd_to_lbp=usd_to_lbp, second_party=second_party, user_id=user_id)

    db.session.add(transaction)
    db.session.commit()

    return jsonify(transaction_schema.dump(transaction)), 201


@transactions.route('/', methods=['GET'], strict_slashes=False)
def get_user_transactions():

    auth_token = extract_auth_token(request)
    if not auth_token:
        abort(401)

    try:
        user_id = decode_token(auth_token)

        transactions = Transaction.query.filter_by(user_id=user_id).all()
        return jsonify(transactions_schema.dump(transactions))

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        abort(401)
