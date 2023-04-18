from flask import Blueprint, request, jsonify, abort
from config.database import db
from config.database import Transaction, transaction_schema, transactions_schema
from services.auth import extract_auth_token, decode_token
import jwt


transactions = Blueprint('transactions', __name__, url_prefix='/transaction')


@transactions.route('/', methods=['POST'])
def create_transaction():

    errors = {}

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

    transaction = Transaction(
        usd_amount=usd_amount, lbp_amount=lbp_amount, usd_to_lbp=usd_to_lbp, user_id=user_id)

    db.session.add(transaction)
    db.session.commit()

    return jsonify(transaction_schema.dump(transaction)), 201


@transactions.route('/', methods=['GET'])
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
