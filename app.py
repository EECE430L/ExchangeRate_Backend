from apis.fluctuations import fluctuations
from apis.statistics import statistics
from apis.authentication import authentication
from apis.users import users
from apis.exchangeRate import exchangeRate
from apis.transactions import transactions
from apis.offers import offers
from flask import Flask
from flask_cors import CORS
from config.database import db
from config.marshmallow import ma
from config.bcrypt import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_CONFIG')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, supports_credentials=True)


db.app = app
db.init_app(app)
ma.app = app
ma.init_app(app)
bcrypt.app = app
bcrypt.init_app(app)


app.register_blueprint(transactions)
app.register_blueprint(exchangeRate)
app.register_blueprint(users)
app.register_blueprint(authentication)
app.register_blueprint(statistics)
app.register_blueprint(fluctuations)
app.register_blueprint(offers)


@app.route('/', methods=['GET'])
def home():
    return 'Welcome to exchange rate backend'


if __name__ == '__main__':
    # app.run(host="0.0.0.0", debug=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
