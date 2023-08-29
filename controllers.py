from flask import jsonify
from middleware import validate_input_middleware, validate_update_middleware
from models import User,db
from flask import  request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from config import generate_confirmation_token, send_reset_email, confirm_token


from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = "signin"

   




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@validate_input_middleware
def signup():
    data = request.get_json()
    user_email = db.session.query(User).filter_by(email=data["email"] ).first()
    if user_email:
        response = jsonify({
        'success': False,
        "message":"You already signed up with that email, log in instead!",
        "token": None,
        "status_code" : 401,
        "user":[]
        })
        return response
    user_input = User(
        firstName = data["firstName"],
        lastName = data["lastName"],
        email = data["email"],
        phoneNumber = data["phoneNumber"],
        password = generate_password_hash(password=data["password"], method="pbkdf2:sha256", salt_length=8)        
    )
    db.session.add(user_input)
    db.session.commit()
    # token generation and confirmation in data base 
   
    token = generate_confirmation_token(user_input.id)
    print(token)
    confirm = confirm_token(token)
    print(confirm)
    response = jsonify({
    'success': True,
    "message":"sign up successful!",
    "token": None,
    "status_code" : 401,
    "user":[]
    })
    return response


#signin and login route
def signin():
    data = request.get_json()
    password = data["password"]
    users =  db.session.query(User).filter_by(email=data["email"] ).first()
    if not users and check_password_hash(users.password, password):
        response = jsonify({
            'success': True,
            "message":"Email doesnt exist or pasword is incorrect, Try again!",
            "token": None,
            "status_code" : 401,
            "user":[]
            })
        return response
    login_user(users)
    response = jsonify({
    'success': True,
    "message":"You are successfully logged in!",
    "token": None,
    "status_code" : 200,
    "user":[]
    })
    return response



@login_required
def password_reset():
    data = request.get_json()
    email = data["email"]
    user_email =  db.session.query(User).filter_by(email=email ).first()
    if not user_email:
        response = jsonify({
        'success': False,
        "message":"Email doesn't doesn't exist!",
        "token": None,
        "status_code" : 401,
        "user":[]
        })
        return response
    token = generate_confirmation_token(user_email.id)
    #the send_reset_email function will send a token to the provided email
    send_reset_email(email, token, user_email.firstName)
    
    response = jsonify({
    'success': True,
    "message":"You!",
    "token": None,
    "status_code" : 401,
    "user":[]
    })
    return response

@login_required
def update_password(token):
    try:
        data = request.get_json()
        existing_password = data["Password"]
        new_password = data["Newpassword"]
        user_id = confirm_token(token)
        user = db.session.query(User).filter_by(id=user_id).first()
        check_user = check_password_hash(user.password, existing_password)
        if not check_user:
            response = jsonify({
            'success': True,
            "message":"existing password doesn't exist!",
            "token": None,
            "status_code" : 401,
            "user":[]
            })
            return response
        user.password = generate_password_hash(new_password, method="pbkdf2:sha256", salt_length=8)
        db.session.commit()
        response = jsonify({
        'success': True,
        "message":"password is successfully updated!",
        "token": None,
        "status_code" : 401,
        "user":[]
        })
        return response
    except Exception:
        response = jsonify({
    'success': False,
    "message":"Sorry unexpected error trying to update password, Try again!",
    "token": None,
    "status_code" : 401,
    "user":[]
    })
    return response

@login_required
def pasword_change():
    data = request.get_json("password")
    new_password = data["password"]
    if not new_password:
        return jsonify("message : new password required")    
    hashed_password = generate_password_hash(password=new_password, method="pbkdf2:sha256", salt_length=8)
    current_user.password = hashed_password
    db.session.commit()
    response = jsonify({
        'success': True,
        "message":"password successfully changed!",
        "token": None,
        "status_code" : 401,
        "user":[]
        })
    return response

@validate_update_middleware
def update_user(token):
    user_id = confirm_token(token)
    user = db.session.query(User).filter_by(id=user_id).first()
    
    if not user:
        response = jsonify({
        'success': True,
        "message":"User not found!",
        "token": None,
        "status_code" : 401,
        "user":[]
    })
        return response
    
    data = request.get_json()
    
    if 'firstName' in data:
        user.firstName = data['firstName']
    if 'lastName' in data:
        user.lastName = data['lastName']
    if 'email' in data:
        user.email = data['email']
    if 'phoneNumber' in data:
        user.phoneNumber = data['phoneNumber']

    
    db.session.commit()

    response = jsonify({
        'success': True,
        "message":f"{data}update is successful!",
        "token": None,
        "status_code" : 200,
        "user":[]
        })
    return response


def user_infor(token):
    user_id = confirm_token(token)
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        response = jsonify({
        'success': True,
        "message":"User not found!",
        "token": None,
        "status_code" : 401,
        "user":[]
        })
        return response
    response = jsonify({
    'success': True,
    "message":"Here is your information!",
    "token": None,
    "status_code" : 200,
    "user":[
        {
            "firstname":user.firstName,
            "lastname":user.lastName,
            "email":user.email,
            "phonenumber":user.phoneNumber,
            "createdAt":user.event_time
        }
    ]
    })
    return response