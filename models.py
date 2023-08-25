from flask_login import UserMixin
from sqlalchemy import TIMESTAMP, func
import uuid
from cryptography.fernet import Fernet
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()





class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(250), nullable=False)
    lastName = db.Column(db.String(250), nullable = False)
    email = db.Column(db.String(250), nullable = False)
    phoneNumber = db.Column(db.String(250), nullable = False)
    password = db.Column(db.String(256), nullable = False)
    event_time = db.Column(TIMESTAMP, server_default=func.now())

   




   # msg = MIMEText(f"click on the link to reset your password:\n\n\n\n{request.url_root}reset_password/{comfirm_token}")
    # msg["Subject"] = 'Password Reset Request'
    # msg["From"] = sender_email
    # msg["To"] = user_email

    # try:
    #     server = smtplib.SMTP(smtp_server, smtp_port)
    #     server.starttls()
    #     server.login(sender_email, sender_password)
    #     server.sendmail(sender_email, [user_email], msg.as_string())
    #     server.quit()
    #     return True
    # except Exception as e:
    #     print(str(e))
    #     return False
