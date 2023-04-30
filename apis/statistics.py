from flask import Blueprint, jsonify
import datetime
from config.database import Transaction
from services.utils import getExchangeRates
import pytz


statistics = Blueprint('statistics', __name__, url_prefix='/statistics')


@statistics.route('/todays-transactions', methods=['GET'], strict_slashes=False)
def get_todays_transactions(request):

    args = request.args
    startYear = int(args.get('startYear'))
    startMonth = int(args.get('startMonth'))
    startDay = int(args.get('startDay'))
    endYear = int(args.get('endYear'))
    endMonth = int(args.get('endMonth'))
    endDay = int(args.get('endDay'))

    try:
        START_DATE = datetime.datetime(startYear, startMonth, startDay)
        END_DATE = datetime.datetime(endYear, endMonth, endDay)
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use yyyy-mm-dd."}), 400

    now = datetime.datetime.now(pytz.timezone('Asia/Beirut'))
    START_DATE = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    END_DATE = now

    numberOfUSDtoLBPTransactions = Transaction.query.filter(
        Transaction.added_date.between(
            START_DATE, END_DATE, Transaction.usd_to_lbp == True
        )).count()

    numberOfLBPtoUSDTransactions = Transaction.query.filter(
        Transaction.added_date.between(
            START_DATE, END_DATE), Transaction.usd_to_lbp == False
    ).count()

    response = {
        "num_usd_to_lbp_transactions": numberOfUSDtoLBPTransactions,
        "num_lbp_to_usd_transactions": numberOfLBPtoUSDTransactions
    }

    return jsonify(response), 200


@ statistics.route('/rates-percent-change', methods=['GET'], strict_slashes=False)
def get_rates_percent_change(request):

    args = request.args
    startYear = int(args.get('startYear'))
    startMonth = int(args.get('startMonth'))
    startDay = int(args.get('startDay'))
    endYear = int(args.get('endYear'))
    endMonth = int(args.get('endMonth'))
    endDay = int(args.get('endDay'))

    try:
        START_DATE_BEGGINING = datetime.datetime(
            startYear, startMonth, startDay)
        END_DATE_END = datetime.datetime(endYear, endMonth, endDay)
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use yyyy-mm-dd."}), 400

    START_DATE_END = START_DATE_BEGGINING + datetime.timedelta(days=1)
    END_DATE_START = END_DATE_END - datetime.timedelta(days=1)

    startExchangeRate = getExchangeRates(START_DATE_BEGGINING, START_DATE_END)
    endExchangeRate = getExchangeRates(
        START_DATE_END, END_DATE_START)

    changeUSDtoLBP = None
    if (startExchangeRate[0] != 0):
        changeUSDtoLBP = (
            (endExchangeRate[0] - startExchangeRate[0]) / startExchangeRate[0]) * 100

    changeLBPtoUSD = None
    if (startExchangeRate[1] != 0):
        changeLBPtoUSD = (
            (endExchangeRate[1] - startExchangeRate[1]) / startExchangeRate[1]) * 100

    response = {
        "percent_change_USD_to_LBP": changeUSDtoLBP,
        "percent_change_LBP_to_USD": changeLBPtoUSD
    }

    return jsonify(response), 200


# last period volume
# percentiles
# average transaction amount
# average transaction amount per user
