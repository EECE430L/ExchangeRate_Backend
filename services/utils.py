from config.database import Transaction
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
import os


# Helper function to get the exchange rates

def getExchangeRates(START_DATE, END_DATE):
    usd_to_lbp_transactions = Transaction.query.filter(
        Transaction.added_date.between(
            START_DATE, END_DATE), Transaction.usd_to_lbp == True
    ).all()
    usd_to_lbp_rate = 0
    for transaction in usd_to_lbp_transactions:
        if (transaction.usd_amount*len(usd_to_lbp_transactions) != 0):
            usd_to_lbp_rate += (transaction.lbp_amount /
                                (transaction.usd_amount * len(usd_to_lbp_transactions)))

    usd_to_lbp_rate = round(usd_to_lbp_rate, 2)

    lbp_to_usd_transactions = Transaction.query.filter(
        Transaction.added_date.between(
            START_DATE, END_DATE), Transaction.usd_to_lbp == False
    ).all()
    lbp_to_usd_rate = 0
    for transaction in lbp_to_usd_transactions:
        if (transaction.usd_amount*len(lbp_to_usd_transactions) != 0):
            lbp_to_usd_rate += (transaction.lbp_amount /
                                (transaction.usd_amount * len(lbp_to_usd_transactions)))
    lbp_to_usd_rate = round(lbp_to_usd_rate, 2)

    return usd_to_lbp_rate, lbp_to_usd_rate


# Code provided by ChatGPT
# Helper function to send an email

def send_email(to_email, subject, content, attachment=None):
    msg = MIMEMultipart()
    sender = os.environ.get('EMAIL')
    msg['From'] = sender
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(content, 'plain'))

    if attachment:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(attachment.getvalue())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="transactions.xlsx"')
        msg.attach(part)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, os.environ.get('EMAIL_PASSWORD'))
            server.sendmail(sender, to_email, msg.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")
