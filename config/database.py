from config.marshmallow import ma
from config.bcrypt import bcrypt
from flask_sqlalchemy import SQLAlchemy
import datetime
import pytz

db = SQLAlchemy()
# DB_CONFIG = 'mysql+pymysql://root:Rorokassab2002!@localhost:3306/exchange'


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'ExchangeRate'}
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True)
    hashed_password = db.Column(db.String(128))
    email = db.Column(db.String(50), unique=True)

    def __init__(self, user_name, password, email):
        super(User, self).__init__(user_name=user_name)
        self.hashed_password = bcrypt.generate_password_hash(password)
        self.email = email


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_name", "email")
        model = User


user_schema = UserSchema()


class Transaction(db.Model):
    __tablename__ = 'transaction'
    __table_args__ = {'schema': 'exchangeRate'}
    id = db.Column(db.Integer, primary_key=True)
    usd_amount = db.Column(db.Float)
    lbp_amount = db.Column(db.Float)
    usd_to_lbp = db.Column(db.Boolean)
    added_date = db.Column(db.DateTime)
    second_party = db.Column(db.String(30), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'ExchangeRate.user.id'), nullable=True)

    def __init__(self, usd_amount, lbp_amount, usd_to_lbp, user_id=None, second_party=None):
        super(Transaction, self).__init__(usd_amount=usd_amount,
                                          lbp_amount=lbp_amount, usd_to_lbp=usd_to_lbp,
                                          user_id=user_id,
                                          second_party=second_party,
                                          added_date=datetime.datetime.now(
                                              pytz.timezone('Asia/Beirut')))


class TransactionSchema(ma.Schema):
    class Meta:
        fields = ("id", "usd_amount", "lbp_amount",
                  "usd_to_lbp", "user_id", "added_date", "second_party")
        model = Transaction


transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)


class Offer(db.Model):
    __tablename__ = 'Offer'
    __table_args__ = {'schema': 'exchangeRate'}
    id = db.Column(db.Integer, primary_key=True)
    offerer = db.Column(db.String(30))
    receiver = db.Column(db.String(30))
    offered_amount = db.Column(db.Float)
    requested_amount = db.Column(db.Float)
    usd_to_lbp = db.Column(db.Boolean)

    def __init__(self, offerer, receiver, offered_amount, requested_amount, usd_to_lbp):
        super(Offer, self).__init__(offerer=offerer, receiver=receiver,
                                    offered_amount=offered_amount, requested_amount=requested_amount, usd_to_lbp=usd_to_lbp)


class OfferSchema(ma.Schema):
    class Meta:
        fields = ("id", "offerer", "receiver", "offered_amount",
                  "requested_amount", "usd_to_lbp")
        model = Offer


offer_schema = OfferSchema()
offers_schema = OfferSchema(many=True)
