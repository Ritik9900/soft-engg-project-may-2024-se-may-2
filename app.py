from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_restful import Api
from backend.models import *
from datetime import timedelta


def start_app():
    app = Flask(__name__, template_folder="templates")
    app.config["SECRET_KEY"] = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///backend.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.app_context().push()
    app.config["JWT_SECRET_KEY"] = "secret"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=10)
    jwt = JWTManager(app)
    app.app_context().push()

    CORS(app)

    # from backend.views import views

    # with app.app_context():
    #     app.register_blueprint(views, url_prefix="/")

    from backend.api import api_bp

    with app.app_context():
        app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()
    return app, jwt

app, jwt = start_app()

if __name__ == "__main__":
    app.run(debug=True)
