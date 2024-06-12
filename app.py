from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_restful import Api
from backend.models import db
from datetime import timedelta



def start_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///backend.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    app.app_context().push()
    app.config['JWT_SECRET_KEY'] = 'secret'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours = 10)
    jwt = JWTManager(app)
    app.app_context().push()



    CORS(app)
    
    API = Api(app)
    app.app_context().push()
    
    from backend.views import views
    with app.app_context():
        app.register_blueprint(views, prefix = '/')
    from backend.api import api
    with app.app_context():
        app.register_blueprint(api, url_prefix = '/api')
    
    create_database(app)
    return app,API,jwt

def create_database(app):
    with app.app_context():
        db.create_all()
    print('Database created')         
    return True

app,API,jwt = start_app()



if __name__ == '__main__':
    app.run(debug=True)