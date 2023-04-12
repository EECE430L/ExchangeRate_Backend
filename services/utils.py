from models.transaction import Transaction


def getExchangeRates(START_DATE, END_DATE):
    usd_to_lbp_transactions = Transaction.query.filter(
        Transaction.added_date.between(START_DATE, END_DATE), Transaction.usd_to_lbp == True
        ).all()
    usd_to_lbp_rate = 0
    for transaction in usd_to_lbp_transactions:
        usd_to_lbp_rate += (transaction.lbp_amount / (transaction.usd_amount * len(usd_to_lbp_transactions)))
    usd_to_lbp_rate = round(usd_to_lbp_rate, 2)

    lbp_to_usd_transactions = Transaction.query.filter(
        Transaction.added_date.between(START_DATE, END_DATE), Transaction.usd_to_lbp == False
        ).all()
    lbp_to_usd_rate = 0
    for transaction in lbp_to_usd_transactions:
        lbp_to_usd_rate += (transaction.lbp_amount / (transaction.usd_amount * len(lbp_to_usd_transactions)))
    lbp_to_usd_rate = round(lbp_to_usd_rate, 2)
    
    return usd_to_lbp_rate, lbp_to_usd_rate
