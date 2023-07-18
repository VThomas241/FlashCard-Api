from flask import request, current_app as app
from flask_restx import Namespace, Resource, fields, abort
from app.core.database import Session
from app.core.models import User

import jwt,bcrypt
from datetime import datetime,timedelta
from app.core.utils.validators import LoginSchema
from app.core.utils.swagger import login_details, token
from app.core.utils.exceptions import InvalidDetailsException,NotFoundException

login = Namespace('auth', 'Endpoints for authorization',path='/login')

@login.route('/')
class LoginResource(Resource):

    @login.expect(login_details)
    @login.marshal_with(token)
    @login.response(400,'Invalid Details')
    @login.response(404,'User Not Found')
    @login.response(500,'Internal Server Error')
    def post(self):
        data = request.get_json()
        errors = LoginSchema.validate(data)
        if errors : raise InvalidDetailsException(errors)

        email, password = data.get('email'), data.get('password')

        with Session() as session:
            user = session.query(User).filter_by(email=email).first()
            if not user: raise NotFoundException('User {}'.format(user.id))

            check = bcrypt.checkpw(
                bytes(password, encoding='UTF-8'),
                bytes(user.password, encoding='UTF-8')
            )

            if not check: raise InvalidDetailsException({'errors': 'Invalid Password'})

            payload = {'id': user.id}
            payload['iss'] = 'FlashCardAppVivek'
            payload['iat'] = datetime.utcnow()
            payload['exp'] = datetime.utcnow() + timedelta(days=100)

            token = jwt.encode(
                payload,
                key=app.config['SECRET_KEY'],
                algorithm='HS256'
            )

            return {'token': token}
