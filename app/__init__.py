from flask_restx import Api

from werkzeug.exceptions import HTTPException,InternalServerError
from app.core.utils.exceptions import CustomException, InvalidDetailsException

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