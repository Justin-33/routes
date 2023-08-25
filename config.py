from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from email.mime.text import MIMEText
from flask import request
from flask_mail import Mail, Message


mail_token_password = "rkcvqdivhkotrovy"

SECRET_KEY = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

def generate_confirmation_token(user_id, expiration=86400):
    """ generate comfirmation token for newly registered users """
    s = Serializer(SECRET_KEY, expiration)
    return s.dumps(user_id).decode('utf-8')

def confirm_token(token):
    """ load token generated add confirm token to database """
    s = Serializer(SECRET_KEY)

    try:
        data = s.loads(token.encode('utf-8'))
        return data
    except Exception:
        return None

    
mail = Mail()

MAIL_SERVER = "smtp.gmail,com"
MAIL_PORT = 587
MAIL_USE_TLS  = True
MAIL_PASSWORD = mail_token_password
MAIL_DEFAULT_SENDER = "nimotaorg661@gmail.com"


def send_reset_email(email, token, name):
    msg = Message(
        subject="reset email token",
    body = f"Hello {name}\n\nclick on the link to reset your password:\n\n\n\n{request.url_root}reset_password/{token}",
    recipients = email
)
    mail.send(msg)