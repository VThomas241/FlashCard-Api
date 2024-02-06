from flask import request,make_response as mk
from flask_restx import Namespace, Resource

from app.core.models import Deck
from app.core.utils.validators import DeckSchema
from app.core.utils.exceptions import InvalidDetailsException
from app.core.utils.protected import authorized
from app.core.utils.swagger import deckSwagger

decks = Namespace('decks', 'Endpoints for decks',path='/decks')

@decks.route('/')
class DecksResource(Resource):
    @decks.doc(security='apikey')
    @decks.response(401, 'Unauthorized')
    @decks.response(500, 'Internal Server Error')
    @decks.marshal_list_with(deckSwagger.outputModel)
    @authorized
    def get(self, user, session):
        decks = session.query(Deck).filter_by(id=user.id).all()
        tags = [ deck.tags for deck in decks ]
        return decks

    @decks.doc(security='apikey')
    @decks.response(400, 'Invalid Details')
    @decks.response(401, 'Unauthorized')
    @decks.response(500, 'Internal Server Error')
    @decks.expect(deckSwagger.inputModel)
    @decks.marshal_with(deckSwagger.outputModel, code=201)
    @authorized
    def post(self, user, session):
        data = request.get_json()
        errors = DeckSchema().validate(data)
        if errors: raise InvalidDetailsException(errors)
        name = data.get('name')

        if session.query(Deck).filter_by(name=name).first():
            raise InvalidDetailsException({'error':'Deck already exists'})

        deck = Deck(user_id=user.id, name=name)
        deck.tags = []
        session.add(deck)
        session.commit()
# Session commit before returning may cause tags to be removed from memory
# and may need to be loaded back into memory
        return deck