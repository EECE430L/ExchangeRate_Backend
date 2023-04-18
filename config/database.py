from config.marshmallow import ma
from config.bcrypt import bcrypt
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
# DB_CONFIG = 'mysql+pymysql://root:Rorokassab2002!@localhost:3306/exchange'


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'ExchangeRate'}
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True)
    hashed_password = db.Column(db.String(128))

    def __init__(self, user_name, password):
        super(User, self).__init__(user_name=user_name)
        self.hashed_password = bcrypt.generate_password_hash(password)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_name")
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
    user_id = db.Column(db.Integer, db.ForeignKey(
        'ExchangeRate.user.id'), nullable=True)

    def __init__(self, usd_amount, lbp_amount, usd_to_lbp, user_id=None):
        super(Transaction, self).__init__(usd_amount=usd_amount,
                                          lbp_amount=lbp_amount, usd_to_lbp=usd_to_lbp,
                                          user_id=user_id,
                                          added_date=datetime.datetime.now())


class TransactionSchema(ma.Schema):
    class Meta:
        fields = ("id", "usd_amount", "lbp_amount",
                  "usd_to_lbp", "user_id", "added_date")
        model = Transaction


transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
