from flask import Blueprint, request, jsonify, abort
from config.database import db
from config.database import Transaction, transaction_schema, transactions_schema
from config.database import User, Offer, offers_schema, offer_schema
from services.auth import extract_auth_token, decode_token
from services.utils import send_email
import jwt


offers = Blueprint('offers', __name__, url_prefix='/offer')


@offers.route('/', methods=['POST'], strict_slashes=False)
def send_offer():

    auth_token = extract_auth_token(request)
    sender_id = None
    if auth_token:
        try:
            sender_id = decode_token(auth_token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            abort(401)
    else:
        return jsonify({"auth_token": "No token was provided"}), 401

    errors = {}

    if ('usd_to_lbp' not in request.json):
        errors['usd_to_lbp'] = 'boolean is missing'
    elif (type(request.json['usd_to_lbp']) != bool):
        errors['usd_to_lbp'] = 'must be a boolean'

    if ('receiver' not in request.json):
        errors['receiver'] = 'string is missing'
    elif (type(request.json['receiver']) != str):
        errors['receiver'] = 'must be a string'

    if ('amount_requested' not in request.json):
        errors['amount_requested'] = 'float is missing'
    elif (type(request.json['amount_requested']) != int and type(request.json['amount_requested']) != float):
        errors['amount_requested'] = 'must be an integer or a float'

    if ('amount_offered' not in request.json):
        errors['amount_offered'] = 'float is missing'
    elif (type(request.json['amount_offered']) != int and type(request.json['amount_offered']) != float):
        errors['amount_offered'] = 'must be an integer or a float'

    receiver = request.json['receiver']
    usd_to_lbp = request.json['usd_to_lbp']
    amount_requested = request.json['amount_requested']
    amount_offered = request.json['amount_offered']

    foundSender = User.query.filter_by(id=sender_id).first()
    foundReceiver = User.query.filter_by(user_name=receiver).first()

    if (not foundSender):
        abort(404)

    if (not foundReceiver):
        return jsonify({"receiver": f"A user with username {receiver} was not found"}), 404
    elif (foundReceiver.id == sender_id):
        return jsonify({"receiver": "You cannot send an offer to yourself"}), 400

    senderUsername = foundSender.user_name
    receiverUsername = foundReceiver.user_name

    offer = Offer(offerer=senderUsername, receiver=receiverUsername,
                  offered_amount=amount_offered, requested_amount=amount_requested, usd_to_lbp=usd_to_lbp)

    db.session.add(offer)
    db.session.commit()

    return jsonify(offer_schema.dump(offer)), 201


@offers.route('/sent', methods=['GET'], strict_slashes=False)
def get_all_user_sended_offers():

    auth_token = extract_auth_token(request)
    sender_id = None
    if auth_token:
        try:
            sender_id = decode_token(auth_token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            abort(401)
    else:
        return jsonify({"auth_token": "No token was provided"}), 401

    sender = User.query.filter_by(id=sender_id).first()

    if (not sender):
        abort(404)

    offers = Offer.query.filter_by(offerer=sender.user_name).all()

    return jsonify(offers_schema.dump(offers)), 200


@offers.route('/received', methods=['GET'], strict_slashes=False)
def get_all_user_received_offers():

    auth_token = extract_auth_token(request)
    receiver_id = None
    if auth_token:
        try:
            receiver_id = decode_token(auth_token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            abort(401)
    else:
        return jsonify({"auth_token": "No token was provided"}), 401

    receiver = User.query.filter_by(id=receiver_id).first()

    if (not receiver):
        abort(404)

    offers = Offer.query.filter_by(receiver=receiver.user_name).all()

    return jsonify(offers_schema.dump(offers)), 200


@offers.route('/process-offer', methods=['POST'], strict_slashes=False)
def process_offer():

    auth_token = extract_auth_token(request)
    user_id = None
    if auth_token:
        try:
            user_id = decode_token(auth_token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            abort(401)
    else:
        return jsonify({"auth_token": "No token was provided"}), 401

    errors = {}

    if ('offer_id' not in request.json):
        return jsonify({errors["offer_id"]: "string is missing"}), 400
    elif (type(request.json['offer_id']) != int):
        return jsonify({errors["offer_id"]: "must be an integer"}), 400

    if ('accepted' not in request.json):
        return jsonify({errors["accepted"]: "boolean is missing"}), 400
    elif (type(request.json['accepted']) != bool):
        return jsonify({errors["accepted"]: "must be a boolean"}), 400

    offer_id = request.json['offer_id']
    accepted = request.json['accepted']

    offer = Offer.query.filter_by(id=offer_id).first()

    if (not offer):
        return jsonify({"offer_id": f"No offer with id {offer_id} was found"}), 404

    sender_username = offer.offerer
    receiver_username = offer.receiver
    sender = User.query.filter_by(user_name=sender_username).first()
    receiver = User.query.filter_by(user_name=receiver_username).first()

    if (not sender):
        return jsonify({"offer_id": f"No user with username {sender_username} was found"}), 404
    elif (not receiver):
        return jsonify({"offer_id": f"No user with username {receiver_username} was found"}), 404

    sender_id = sender.id
    receiver_id = receiver.id

    if (receiver_id != user_id):
        return jsonify({"offer_id": f"User with id {user_id} is not authorized to process this offer"}), 401

    transactionsCreated = None

    if (not accepted):
        send_email(sender.email, "Offer Rejected",
                   f"Your offer with id {offer_id} was rejected by {receiver_username}.")

    else:

        if (offer.usd_to_lbp):
            senderTransaction = Transaction(usd_amount=offer.offered_amount,
                                            lbp_amount=offer.requested_amount,
                                            usd_to_lbp=offer.usd_to_lbp,
                                            second_party=receiver_username,
                                            user_id=sender_id)

            receiverTransaction = Transaction(usd_amount=offer.offered_amount,
                                              lbp_amount=offer.requested_amount,
                                              usd_to_lbp=offer.usd_to_lbp,
                                              second_party=sender_username,
                                              user_id=receiver_id)

            db.session.add(senderTransaction)
            db.session.commit()
            db.session.add(receiverTransaction)
            db.session.commit()

            transactionsCreated = [senderTransaction, receiverTransaction]

            send_email(sender.email, "Offer Accepted",
                       f"Your offer with id {offer_id} was accepted by {receiver_username}.")

        else:
            senderTransaction = Transaction(lbp_amount=offer.offered_amount,
                                            usd_amount=offer.requested_amount,
                                            usd_to_lbp=offer.usd_to_lbp,
                                            second_party=receiver_username,
                                            user_id=sender_id)

            receiverTransaction = Transaction(lbp_amount=offer.offered_amount,
                                              usd_amount=offer.requested_amount,
                                              usd_to_lbp=offer.usd_to_lbp,
                                              second_party=sender_username,
                                              user_id=receiver_id)

            db.session.add(senderTransaction)
            db.session.commit()
            db.session.add(receiverTransaction)
            db.session.commit()

            transactionsCreated = [senderTransaction, receiverTransaction]

            send_email(sender.email, "Offer Accepted",
                       f"Your offer with id {offer_id} was accepted by {receiver_username}.")

    Offer.query.filter_by(id=offer_id).delete()
    db.session.commit()

    return jsonify(transactions_schema.dump(transactionsCreated)), 201
