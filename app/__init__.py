from flask import Flask
from app.extensions import db, jwt
import os
from dotenv import load_dotenv



def create_app():
    app = Flask(__name__)

    from .auth import authBP
    from .views import viewsBP

    load_dotenv()
    app.config.from_prefixed_env()


    #initializing extensions
    db.init_app(app)
    jwt.init_app(app)

    
    app.register_blueprint(authBP, url_prefix="/auth")
    app.register_blueprint(viewsBP)

    
    # ...
    

    return app