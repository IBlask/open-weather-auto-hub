from flask import jsonify
from sqlalchemy.exc import IntegrityError
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from dotenv import load_dotenv
from os import environ

from app import db
from models import Email

# Load environment variables from .env file
load_dotenv()

# Configure logging for SMTP debugging
logging.basicConfig(level=logging.INFO)

def is_valid_email(email_address):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email_address) is not None


def add_email(email_address):
    if not email_address or email_address.isspace():
        return 'Email address is required!', 400
    
    if not is_valid_email(email_address):
        return 'Invalid email address!', 400
    
    try:
        email = Email(email = email_address)
        db.session.add(email)
        db.session.commit()
        return 'Email added successfully!', 200
    except IntegrityError:
        return 'Email address already exists!', 400
    except Exception as e:
        return 'Error adding new email! Please try again.', 500


def delete_email(email_address):
    if not email_address or email_address.isspace():
        return 'Email address is required!', 400

    try:
        email = Email.query.get(email_address)
        if email:
            db.session.delete(email)
            db.session.commit()
            return 'Email deleted successfully!', 200
        return 'Email address not found!', 404
    except Exception as e:
        return 'Error deleting email! Please try again.', 500
    

def get_all_emails():
    emails = Email.query.all()
    return [email.email for email in emails], 200


def send_rain_warning_email(recipient_email, prediction):
    sender_email = environ.get('EMAIL_USERNAME')
    sender_password = environ.get('EMAIL_PASSWORD')
    smtp_host = environ.get('EMAIL_SMTP_HOST')
    smtp_port = environ.get('EMAIL_SMTP_PORT')

    subject = "OWAH: Rain Warning"
    body = f"Warning: Rain is predicted with a probability of {prediction * 100:.2f}%.\n\nYour OpenWeatherAutoHub"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.set_debuglevel(1)  # Enable debug output
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        logging.info('Email sent successfully!')
    except Exception as e:
        logging.error(f'Failed to send email: {e}')
