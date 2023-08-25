#import logging
#import time
from flask import Flask
#from decouple import config
from sqlalchemy_utils import create_database, database_exists
from models import db
from config import mail





from controllers import (
    signup,
    signin,
    password_reset,
    update_password,
    pasword_change,
    update_user,
    login_manager,
    token
)


# Create an instance of Flask app
app = Flask(__name__)
app.config.from_object('config')
#app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
#Configure logging
#logging.basicConfig(level=logging.INFO)

#Configure the database connection
# database_user = config('DATABASE_USER')
# database_password = config('DATABASE_PASSWORD')
# database_host = config('DATABASE_HOST')
# database_port = int(config('DATABASE_PORT')) 
# database_name = config('DATABASE_NAME')
# server_port = config('SERVER_PORT')

# database_user = "root"
# database_password = "examplepassword"
# database_host = "db"
# database_port = "3306" 
# database_name = "your_database_name"
# server_port = "5013"

# Print the database details
# logging.info(f'Database details:')
# logging.info(f'  Host: {database_host}')
# logging.info(f'  Port: {database_port}')
# logging.info(f'  Name: {database_name}')
# logging.info(f'  User: {database_user}')
# logging.info(f'  password: {database_password}')

# Configure the Flask app with SQLAlchemy
#app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create an instance of SQLAlchemy
with app.app_context():
    db.init_app(app)
    db.create_all()

with app.app_context():
    login_manager.init_app(app)

with app.app_context():
    secret = app.config['SECRET_KEY']

with app.app_context():
    mail.init_app(app)

# Function to establish the database connection
# def connect_to_database():
#     retries = 0
#     max_retries = 10
#     connected = False

    #with app.app_context():
        #while retries < max_retries:
            #try:
                 #if not database_exists(f"mysql+pymysql://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}"):
                  #   create_database(f"mysql+pymysql://{database_user}:{database_password}@{database_host}:{database_port}")
                  #  logging.info(f'Created database: {database_name}')
                
        #         db.create_all()
        #         logging.info('Connected to the database.')
        #         connected = True
        #         break
        #     except Exception as e:
        #         logging.error(f'Error connecting to the database: {e}')
        #         retries += 1
        #         logging.info(f'Retrying in 10 seconds...')
        #         time.sleep(10)

        # if not connected:
        #     logging.error('Failed to connect to the database. Exiting...')
        #     exit(1)

# Call the connect_to_database function to establish the connection
#connect_to_database()

# Define a route
app.add_url_rule("/auth/signup",  "signup",  signup, methods=["POST"])
app.add_url_rule("/auth/signin", "signin", signin, methods=["POST"])
app.add_url_rule("/auth/password/change", "password_change", pasword_change, methods=["POST"])
app.add_url_rule("/auth/password/reset", "password_reset", password_reset, methods=["POST"])
app.add_url_rule(f"/auth/update_password/<token>", "update_password", update_password, methods=["POST"])
app.add_url_rule("/me/<token>", "updated_user", update_user, methods=["POST"])


if __name__ == '__main__':
    # Start the server
    app.run(debug=True)
