from flask import Flask


def create_app():
    app = Flask(__name__)
    from .auth import authBP
    from .views import viewsBP

    app.register_blueprint(authBP, url_prefix="/auth")
    app.register_blueprint(viewsBP)

    # ...
    

    return app