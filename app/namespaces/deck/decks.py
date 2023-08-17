from flask import request,make_response as mk
from flask_restx import Namespace, Resource

from app.core.models import Deck
from app.core.utils.validators import DeckSchema
from app.core.utils.exceptions import InvalidDetailsException
from app.core.utils.protected import authorized
from app.core.utils.swagger import deck_in,deck_out

decks = Namespace('decks', 'Endpoints for decks',path='/decks')

@decks.route('/')
class DecksResource(Resource):
    @decks.doc(security='apikey')
    @decks.response(401, 'Unauthorized')
    @decks.response(500, 'Internal Server Error')
    @decks.marshal_list_with(deck_out)
    @authorized
    def get(self, user, session):
        return user.decks

    @decks.doc(security='apikey')
    @decks.expect(deck_in)
    @decks.response(400, 'Invalid Details')
    @decks.response(401, 'Unauthorized')
    @decks.response(500, 'Internal Server Error')
    @decks.marshal_with(deck_out, code=201)
    @authorized
    def post(self, user, session):
        data = request.get_json()
        errors = DeckSchema().validate(data)
        if errors: raise InvalidDetailsException(errors)
        name = data.get('name')

        if session.query(Deck).filter_by(name=name).first():
            raise InvalidDetailsException({'error':'Deck already exists'})

        deck = Deck(user_id=user.id, name=name)
        session.add(deck)
        session.commit()

        return deck