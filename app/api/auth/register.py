from flask import request
from flask_restx import Namespace, Resource

from app.utils.validators import RegisterSchema
from app.utils.exceptions import  InvalidDetailsException,UserAlreadyExists
from app.core.database import Session
from app.core.models import User
from app.utils.swagger import registerSwagger
import bcrypt


register = Namespace('auth', 'Endpoints for authorization',path='/register')

@register.route('/')
class RegisterResource(Resource):

    @register.expect(registerSwagger.model)
    @register.response(500, 'Internal Server Error')
    @register.response(403, 'Account already exists')
    @register.response(400, 'Invalid User Details')
    @register.response(201, 'Registration successful')
    def post(self):
        data = request.get_json()

        errors = RegisterSchema().validate(data)
        if errors: raise InvalidDetailsException(errors)

        user_name, email, password = (
            data.get('user_name'),
            data.get('email'),
            data.get('password')
        )

        password = bcrypt.hashpw(
            bytes(password, encoding='UTF-8'),
            bcrypt.gensalt()
        )
        
        with Session() as session:
            if session.query(User).filter_by(email=email).first(): 
                raise UserAlreadyExists({'error':'User already exists'})

            session.add(User(
                user_name=user_name,
                email=email,
                password=str(password,encoding='UTF-8')))
            
            session.commit()
        
        return {'data':{'message': "Registration for {} was successfull".format(email)}}, 201