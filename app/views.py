from flask import Flask, render_template, Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, current_user

viewsBP = Blueprint('views', __name__)

@viewsBP.route('/', methods=['GET'])
def home():
    return render_template('workout/index.html')

@viewsBP.route('/dashboard', methods=['GET'])
def dashBoard():
    return jsonify({'success': 'You have successfully connected to the dashboard page.'})

@viewsBP.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    return jsonify({"message": "success","user_details":{"username": current_user.username, "email": current_user.email}})

@viewsBP.route('/main', methods=['GET'])
@jwt_required()
def main():
    return render_template('workout/main.html')
