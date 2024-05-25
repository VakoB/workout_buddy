from flask import Flask, request, Blueprint, render_template, jsonify, redirect, url_for
from app.models import User, TokenBlocklist
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity

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

            return redirect(url_for('auth.login'))
            

        
        elif user is not None:
            return redirect(url_for('auth.login'))
        

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
