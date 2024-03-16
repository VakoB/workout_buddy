from flask import Flask, request, Blueprint, render_template

authBP = Blueprint('auth', __name__)

@authBP.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('auth/login.html')

@authBP.route('/register', methods=['POST', 'GET'])
def register():
    return render_template('auth/register.html')
