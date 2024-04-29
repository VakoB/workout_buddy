from flask import Flask, request, Blueprint, render_template, jsonify
from app.models import User
from flask_jwt_extended import create_access_token, create_refresh_token

authBP = Blueprint('auth', __name__)

@authBP.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    elif request.method == 'POST':
            
        data = request.get_json()

        user = User.get_user_by_username(username=data.get('username'))

        if user and (user.check_password(password=data.get('password'))):

            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            return jsonify(
                {
                    "message": "Logged in",
                    "tokens": {
                        "access": access_token,
                        "refresh": refresh_token
                    }
                }, 200
            )
        return jsonify(
            {
                "error": "Invalid username or password."
            }, 400
        )

@authBP.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'GET':
        return render_template('auth/register.html')
    elif request.method == 'POST':

        data = request.get_json()
        user = User.get_user_by_username(username=data.get('username'))

        if user is None:
            new_user = User(
                username = data.get('username'),
                email = data.get('email')
            )
            new_user.set_password(data.get('password'))

            new_user.save()
            print('user created')
            # redirect to the main page (or sign in page)
            return jsonify({'suceess': 'the user was created.'}), 201
            

        
        elif user is not None:
            return jsonify({'error': 'the user already exists.'}), 403
        

    
