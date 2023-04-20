from flask import Blueprint, jsonify
import datetime
from config.database import Transaction
from services.utils import getExchangeRates


statistics = Blueprint('statistics', __name__, url_prefix='/statistics')


@statistics.route('/todays-transactions', methods=['GET'], strict_slashes=False)
def get_todays_transactions():
    now = datetime.datetime.now()
    START_DATE = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    END_DATE = now

    numberOfUSDtoLBPTransactions = Transaction.query.filter(
        Transaction.added_date.between(
            START_DATE, END_DATE), Transaction.usd_to_lbp == True
    ).count()
    numberOfLBPtoUSDTransactions = Transaction.query.filter(
        Transaction.added_date.between(
            START_DATE, END_DATE), Transaction.usd_to_lbp == False
    ).count()

    response = {
        "num_usd_to_lbp_transactions": numberOfUSDtoLBPTransactions,
        "num_lbp_to_usd_transactions": numberOfLBPtoUSDTransactions
    }

    return jsonify(response), 200


@statistics.route('/rates-percent-change', methods=['GET'], strict_slashes=False)
def get_rates_percent_change():

    now = datetime.datetime.now()
    YESTERDAY_START = datetime.datetime(
        now.year, now.month, now.day, 0, 0, 0) - datetime.timedelta(days=1)
    YESTERDAY_END = datetime.datetime(
        now.year, now.month, now.day, 0, 0, 0) - datetime.timedelta(seconds=1)
    TODAY_START = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    TODAY_END = now

    yesterdayExchangeRate = getExchangeRates(YESTERDAY_START, YESTERDAY_END)
    todayExchangeRate = getExchangeRates(TODAY_START, TODAY_END)

    changeUSDtoLBP = "Not available: no USD to LBP transactions were done yesterday"
    if (yesterdayExchangeRate[0] != 0):
        changeUSDtoLBP = (
            (todayExchangeRate[0] - yesterdayExchangeRate[0]) / yesterdayExchangeRate[0]) * 100
    changeLBPtoUSD = "Not available : no LBP to USD transactions were done yesterday"
    if (yesterdayExchangeRate[1] != 0):
        changeLBPtoUSD = (
            (todayExchangeRate[1] - yesterdayExchangeRate[1]) / yesterdayExchangeRate[1]) * 100

    response = {
        "percent_change_USD_to_LBP": changeUSDtoLBP,
        "percent_change_LBP_to_USD": changeLBPtoUSD
    }

    return jsonify(response), 200


# last period volume
# percentiles
# average transaction amount
# average transaction amount per user
