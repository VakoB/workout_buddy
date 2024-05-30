from flask import Flask, request, Blueprint, render_template, jsonify, redirect, url_for
from app.models import User, TokenBlocklist
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity, current_user

authBP = Blueprint('auth', __name__)

@authBP.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

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
                "message": "Invalid username or password.",
                "success": False
            }, 400
        )
    
    return render_template('auth/login.html')


@authBP.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':

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

            return jsonify({"message": "created user successfully", "success": True}), 201
            
    
        
        elif user is not None:
            return jsonify({"message": "user already exists.", "success": False}), 409
        
    return render_template('auth/register.html')
        
@authBP.route('/jwtclaims')
@jwt_required()
def jwtClaims():
    claims = get_jwt()
    return jsonify({"message": "success", "claims": claims})
    
@authBP.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity)

    return jsonify({"access_token": new_access_token})


@authBP.route('/logout', methods=['GET'])
@jwt_required(verify_type=False)
def logout_user():
    jwt = get_jwt()

    jti = jwt['jti']

    token_type = jwt['type']

    token_b = TokenBlocklist(jti=jti)

    token_b.save()

    return jsonify({'message': f'{token_type} token revoked successfully'}), 200
