from functools import wraps
from flask import  request



# Input validation middleware
def validate_input_middleware(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        required_fields = ['firstName','lastName', 'email', 'password', 'phoneNumber']
        data = request.get_json()
        if len(data["password"]) < 8:
            return {'error':'Password must be at least 8 characters long'}, 400
        if not any(char.isdigit() for char in data["password"]):
            return {'error':'Password must contain at least one digit'}, 400
        if not any(char.isalpha() for char in data["password"]):
            return {'error':'Password must contain at least one letter'},400

        if "@" and ".com" not in data["email"]:
            return {'error':"invalid input for email"},400
        
        if len(data['phoneNumber']) < 11:
            return {"error": "phone number is incomplete"}, 400
        print(data)

        for field in required_fields:
            if field not in data:
                return {"error": f"Missing required field: {field}"}, 400

        return func(*args, **kwargs)
    
    return wrapper

# Security middleware
def security_middleware(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check user permissions here
        # Example: If the user is not authenticated or doesn't have the required permission, return an error response
        # if not is_user_authenticated() or not has_permission():
        print("security middleware")

        return func(*args, **kwargs)
    
    return wrapper

def validate_update_middleware(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        if "password" in data and len(data["password"]) < 8:
            return {'error':'Password must be at least 8 characters long'}, 400
        if "password" in data and not any(char.isdigit() for char in data["password"]):
            return {'error':'Password must contain at least one digit'}, 400
        if "password" in data and not any(char.isalpha() for char in data["password"]):
            return {'error':'Password must contain at least one letter'},400

        if "email" in data and "@" and ".com" not in data["email"]:
            return {'error':"invalid input for email"},400
        
        if "phoneNumber" in data and len(data['phoneNumber']) < 11:
            return {"error": "phone number is incomplete"}, 400
        print(data)

        return func(*args, **kwargs)
    
    return wrapper
