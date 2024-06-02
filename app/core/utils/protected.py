from functools import wraps
from flask import request,current_app as app
from app.core.database import Session
from app.core.models import User
from app.core.utils.exceptions import UnauthorizedException
from werkzeug.exceptions import InternalServerError
from typing import Callable
import jwt

def authorized(func: Callable):

    @wraps(func)
    def wrapper(*args,**kwargs):

        # Checking if token is present in the header
        auth_header = request.headers.get('Authorization',None)
        if not auth_header: raise UnauthorizedException()

        # Add new exception for not having bearer
        if not auth_header.startswith('Bearer '): raise UnauthorizedException()
        token = auth_header.split(' ')[-1]
        
        try: 
            options={
                'verify_signature':True,
                'require':["exp", "iat", "iss"],
                'verify_exp':'verify_signature',
                'verify_iat':'verify_signature',
                'verify_iss':'verify_signature'

            }
            token_body = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms=['HS256'],
                options=options,
                leeway=300
            )

        except Exception as e:
            raise UnauthorizedException()
        
        user_id = token_body.get('id')

        with Session() as session:
            user:User = session.get(User,user_id)
            if not user: raise UnauthorizedException()
            #? Returning the view function with an additional user_id variable for easy processing
            #? inside the view variable
            return func(*args, user, session, **kwargs)
       
        

    return wrapper
