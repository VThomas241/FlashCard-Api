from werkzeug.exceptions import HTTPException
from typing import Dict,List

class InvalidFilterField(Exception):
    def __init__(self, field, *args: object) -> None:
        self.message = "The model does not contain the field '{}'".format(field)
        super().__init__(self.message,*args)
        
class CustomException(HTTPException):
    '''Custom Exception Class for api exceptions.'''
    pass


class InvalidDetailsException(CustomException):
    '''
    :param errors: Dictionary of errors of type Dict[str:str]
    code: 400
    '''
    code = 400
    name = 'InvalidDetailsException'
    errors: dict
    
    def __init__(self, errors: Dict[str,List[str]]) -> None:
        self.errors = errors

class NotFoundException(CustomException):
    '''
    code: 404
    '''
    code = 404
    name = 'NotFoundException'
    description: str

    def __init__(self, resource: str | None) -> None:
        if resource: self.description = '{} not found'.format(resource)
        else: resource = "The resource you are looking for does not exist"
        
class UnauthorizedException(CustomException):
    '''
    code: 401
    '''
    code = 401
    name = 'UnauthorizedException'
    description = 'You need to have a valid auth token.'

class InvalidTokenException(CustomException):
    '''
    code: 406
    '''
    code = 406
    name = 'InvalidTokenException'
    description = 'Your auth token is invalid.'

class UserAlreadyExists(CustomException):
    '''
    code: 403
    '''
    code = 403
    name = 'UserAlreadyExists'
    description = 'An account with this email already exists'

class BearerNotFound(CustomException):
    '''
    code: 404
    '''
    code = 404
    name = 'BearerNotFound'
    description = "Your auth token is not prefixed by 'Bearer '"

