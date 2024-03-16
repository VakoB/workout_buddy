from flask import Flask, render_template, Blueprint

viewsBP = Blueprint('views', __name__)

@viewsBP.route('/', methods=['GET'])
def home():
    return render_template('workout/index.html')