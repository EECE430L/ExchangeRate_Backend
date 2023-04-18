from flask import Blueprint, request, jsonify
import datetime
from services.utils import getExchangeRates


fluctuations = Blueprint('fluctuations', __name__, url_prefix='/fluctuations')


@fluctuations.route('/', methods=['GET'])
def get_exchangeRateFluctuations():
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

    statistics = {}

    current_date = START_DATE
    while current_date <= END_DATE:
        start_of_period = current_date
        end_of_period = current_date + \
            datetime.timedelta(hours=23, minutes=59, seconds=59)
        usd_to_lbp_rate, lbp_to_usd_rate = getExchangeRates(
            start_of_period, end_of_period)
        start_of_period = start_of_period.strftime("%Y-%m-%d %H:%M:%S")
        end_of_period = end_of_period.strftime("%Y-%m-%d %H:%M:%S")
        if (usd_to_lbp_rate == 0):
            usd_to_lbp_rate = "No Data Available"
        if (lbp_to_usd_rate == 0):
            lbp_to_usd_rate = "No Data Available"
        statistics[start_of_period+'|' +
                   end_of_period] = (usd_to_lbp_rate, lbp_to_usd_rate)
        current_date += datetime.timedelta(days=1)

    return jsonify(statistics), 200
