import os
from dotenv import load_dotenv
import smtplib
import logging
from email.mime.text import MIMEText

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

load_dotenv()

def send_test_email():
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = '30fluffy09@gmail.com'
    receiver_email = 'prakharpalod555@gmail.com'
    password = os.getenv('SMTP_APP_PASSWORD')  

    message = MIMEText('This is a test email sent via Python SMTP client.')
    message['Subject'] = 'Lab 2 - SMTP Test'
    message['From'] = sender_email
    message['To'] = receiver_email

    try:
        logging.info(f"Connecting to SMTP server {smtp_server}:{smtp_port}")
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            server.ehlo()
            logging.info("Starting TLS encryption...")
            server.starttls()
            server.ehlo()
            logging.info("Logging in...")
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            logging.info("Email sent successfully!")
    except Exception as e:
        logging.error(f"SMTP Error: {e}")

if __name__ == "__main__":
    send_test_email()
