from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from werkzeug.exceptions import HTTPException,InternalServerError
from app.core.utils.exceptions import CustomException, InvalidDetailsException
from app.core.config import Config
from app.core.utils.swagger import SwaggerModel
from app.blueprints import ns_list

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    authorizations=authorizations,
    title='Flash Card',
    description='Flash Card app for App Dev 2',
    ordered=True,
    contact='vivekthomasnitro1@gmail.com',
    contact_email='vivekthomasnitro1@gmail.com',
    )

@api.errorhandler(InvalidDetailsException)
def invalidDetails(e):
    return {
        "code": e.code,
        "name": e.name,
        "errors": e.errors,
    },e.code

@api.errorhandler(CustomException)
def customException(e):
    return {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    },e.code

@api.errorhandler(HTTPException)
def httpException(e):
    return {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    },e.code

@api.errorhandler(InternalServerError)
def internalServerError(e):
    return {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    },e.code

@api.errorhandler(Exception)
def exception(e):
    return {
        "code": 500,
        "name": 'InternalServerError',
        "description": str(e),
    },500

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app,origins=[Config.FRONTEND_URL])
    app.config.from_object(Config)
    app.app_context().push()

    api.init_app(app)
    for ns in ns_list: api.add_namespace(ns)
    for model in SwaggerModel.models: api.models[model.name] = model
    return app
