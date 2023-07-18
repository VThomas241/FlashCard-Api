from flask import current_app as app,make_response as mk
from flask_restx.api import current_app as api
from werkzeug.exceptions import Forbidden, BadRequest,Unauthorized,NotFound,InternalServerError,HTTPException,MethodNotAllowed
from app.core.utils.exceptions import CustomException

@api.handle_exception(NotFound)
def notFound(e):
    return {
        "code": e.code,
        "name": e.name,
        "description": "The user/resource you are looking for does not exist.",
    }.e.code

@api.handle_exception(BadRequest)
def badRequest(e):
    return {
        "code": e.code,
        "name": e.name,
        "description": "You have sent a bad request. Please ensure that you have given all the necessary information in the request",
    },e.code


@api.handle_exception(Unauthorized)
def badRequest(e):
    return {
        "code": e.code,
        "name": e.name,
        "description": "You are not authorized to access this resource. If you are trying to get authorized please check that your credenitals are correct.",
    },e.code

@api.handle_exception(MethodNotAllowed)
def methodNotAllowed(e):
    return {
        "code": e.code,
        "name": e.name,
        "description": "You are not allowed to use this method at this endpoint",
    },e.code


@api.handle_exception(CustomException)
def deckNameException(e):
    return {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    },e.code



@api.handle_exception(HTTPException)
def httpException(e):
    return {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }

@api.handle_exception(InternalServerError)
def internalServerError(e):
    return {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    },e.code
