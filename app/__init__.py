from flask import Flask, jsonify
from app.extensions import db, jwt
import os
from dotenv import load_dotenv
from app.models import User, TokenBlocklist



def create_app():
    app = Flask(__name__)

    from .auth import authBP
    from .views import viewsBP
    from .users import userBP

    load_dotenv()
    app.config.from_prefixed_env()


    #initializing extensions
    db.init_app(app)
    jwt.init_app(app)

    
    app.register_blueprint(authBP, url_prefix="/auth")
    app.register_blueprint(viewsBP)
    app.register_blueprint(userBP, url_prefix="/users")

    # load user
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_headers, _jwt_data):
        identity = _jwt_data['sub']

        return User.query.filter_by(username=identity).one_or_none()


    # additional claims

    # upgrading user to staff so I can
    # easily grant them certain functualities
    # by checking if they're staff

    @jwt.additional_claims_loader
    def make_additional_claims(identity):
        if identity == "vako": return {"is_staff": True}
        return {"is_staff": False}
    
    # jwt error handler

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({"message": "token has expired.", "error": "token_expired"}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Signature verification failed", "error": "invalid_token"}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message": "request does not contain valid token", "error": "authorization_header"}), 401

    # Checks if jwt is revoked
    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header, jwt_data):
        jti = jwt_data['jti']
        
        token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()

        return token is not None
    
    @jwt.revoked_token_loader
    def token_revoked_callback(jwt_header, jwt_data):
        return jsonify({"message": "Token has been revoked :)"})

    return app



