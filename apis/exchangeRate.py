from flask import Blueprint, jsonify
from config.database import db
from services.utils import getExchangeRates
import datetime


exchangeRate = Blueprint('exchangeRate', __name__,
                         url_prefix='/exchangeRate')


@exchangeRate.route('/', methods=['GET'], strict_slashes=False)
def get_exchange_rate():

    START_DATE = datetime.datetime.now() - datetime.timedelta(days=3)
    END_DATE = datetime.datetime.now()

    usd_to_lbp_rate, lbp_to_usd_rate = getExchangeRates(START_DATE, END_DATE)

    response = {
        "usd_to_lbp": usd_to_lbp_rate,
        "lbp_to_usd": lbp_to_usd_rate
    }

    return jsonify(response), 200
