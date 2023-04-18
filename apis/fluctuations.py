from flask import Blueprint, request, jsonify
import datetime
from services.utils import getExchangeRates
from services.fluctuationResponse import fluctuationResponseUsdToLbp, fluctuationResponseLbpToUsd


fluctuations = Blueprint('fluctuations', __name__,
                         url_prefix='/fluctuations')


@fluctuations.route('/usd-to-lbp', methods=['GET'], strict_slashes=False)
def get_exchangeRateFluctuationsUSD():
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

    fluctuations = []

    current_date = START_DATE
    while current_date <= END_DATE:
        start_of_period = current_date
        end_of_period = current_date + \
            datetime.timedelta(hours=23, minutes=59, seconds=59)
        usd_to_lbp_rate, lbp_to_usd_rate = getExchangeRates(
            start_of_period, end_of_period)
        start_of_period = start_of_period.strftime("%Y-%m-%d")
        end_of_period = end_of_period.strftime("%Y-%m-%d")
        if (usd_to_lbp_rate == 0):
            usd_to_lbp_rate = "No Data Available"
        if (lbp_to_usd_rate == 0):
            lbp_to_usd_rate = "No Data Available"

        FluctuationResponseUsdToLbp = fluctuationResponseUsdToLbp(
            start_of_period, end_of_period, usd_to_lbp_rate)
        fluctuations.append(FluctuationResponseUsdToLbp.serialize())
        current_date += datetime.timedelta(days=1)

    return jsonify(fluctuations), 200


@fluctuations.route('/lbp-to-usd', methods=['GET'], strict_slashes=False)
def get_exchangeRateFluctuationsLBP():
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

    fluctuations = []

    current_date = START_DATE
    while current_date <= END_DATE:
        start_of_period = current_date
        end_of_period = current_date + \
            datetime.timedelta(hours=23, minutes=59, seconds=59)
        usd_to_lbp_rate, lbp_to_usd_rate = getExchangeRates(
            start_of_period, end_of_period)
        start_of_period = start_of_period.strftime("%Y-%m-%d")
        end_of_period = end_of_period.strftime("%Y-%m-%d")
        if (usd_to_lbp_rate == 0):
            usd_to_lbp_rate = "No Data Available"
        if (lbp_to_usd_rate == 0):
            lbp_to_usd_rate = "No Data Available"

        FluctuationResponseLbpToUsd = fluctuationResponseLbpToUsd(
            start_of_period, end_of_period, lbp_to_usd_rate)
        fluctuations.append(FluctuationResponseLbpToUsd.serialize())
        current_date += datetime.timedelta(days=1)

    return jsonify(fluctuations), 200
