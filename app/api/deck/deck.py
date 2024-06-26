from flask import request
from flask_restx import Namespace, Resource

from app.core.models import Deck
from app.utils.validators import DeckSchema
from app.utils.protected import authorized
from app.utils.exceptions import InvalidDetailsException,NotFoundException
from app.utils.swagger import deckSwagger

deck = Namespace(
    'decks',
    'Endpoints for decks',
    path='/decks'
)


@deck.route('/<int:deck_id>')
class DeckResource(Resource):
    @deck.doc(security='apikey')
    @deck.marshal_with(deckSwagger.outputModelWithCards,envelope='data')
    @deck.response(401, 'Unauthorized')
    @deck.response(404, 'Deck Not Found')
    @deck.response(500,'Internal Server Error')
    @authorized
    def get(self, user, session, deck_id):
        deck = session.query(Deck).filter_by(user_id=user.id, id=deck_id).first()
        if not deck: raise NotFoundException('Deck {}'.format(deck_id))

        #? To force lazy loading of cards attribute before returning
        cards = deck.cards
        #? To implement in future (also in swagger.py/deckSwagger class)
        tags = deck.tags
        
        return deck

    @deck.doc(security='apikey')
    @deck.expect(deckSwagger.inputModel)
    @deck.marshal_with(deckSwagger.outputModel,envelope='data')
    @deck.response(400, 'Invalid Deck Details')
    @deck.response(401, 'Unauthorized')
    @deck.response(404, 'Deck Not Found')
    @deck.response(500,'Internal Server Error')
    @authorized
    def put(self, user, session, deck_id):
        #? Parsing and validating data from json request
        data = request.get_json()
        errors = DeckSchema().validate(data)
        if errors : raise InvalidDetailsException(errors)

        deck = session.query(Deck).filter_by(user_id=user.id, id=deck_id).first()
        if not deck: raise NotFoundException('Deck {}'.format(deck_id))

        name = data.get('name')
        if session.query(Deck).filter_by(name=name).first():
            raise InvalidDetailsException({'error':'Deck already exists'})
        
        deck.name = name
        

        '''
            On commit all objects related to that session are expired
            by default thus we cannot return the deck object after committing
            So, we turn it off for this case 
        '''
        session.expire_on_commit = False
        session.commit()
        tags = deck.tags
        return deck
    
    @deck.doc(security='apikey')
    @deck.response(204, 'Deck deleted')
    @deck.response(404, 'Deck Not Found')
    @deck.response(500,'Internal Server Error')
    @authorized
    def delete(self, user, session, deck_id):
        deck = session.query(Deck).filter_by(user_id=user.id, id=deck_id).first()
        if not deck: raise NotFoundException('Deck {}'.format(deck_id))
        
        session.delete(deck)
        session.commit()
        session.close()

        return {'data':{'message': 'Deck with id: {} has been deleted'.format(deck_id)}},204

