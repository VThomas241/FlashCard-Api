from flask_restx import Namespace,Resource
from flask import request

from app.core.models import Card
from app.core.utils.protected import authorized
from app.core.utils.exceptions import InvalidDetailsException,NotFoundException
from app.core.utils.validators import CardSchema
from app.core.utils.swagger import cardSwagger


card = Namespace(
    'cards',
    'Endpoints related to card',
    path='/decks',
    ordered=True
)

card_in = cardSwagger.inputModel
card_out = cardSwagger.outputModel

@card.route('/<int:deck_id>/cards/<int:card_id>')
class CardResource(Resource):
    @card.doc(security='apikey')
    @card.marshal_with(card_out,envelope='data')
    @card.response(404, 'Card Not Found')
    @card.response(500, 'Internal Setver Error')
    @authorized
    def get(self,user,session,deck_id,card_id):
        card = session.query(Card).filter_by(user_id=user.id,deck_id=deck_id,id=card_id).first()
        if not card: raise NotFoundException('Card {}'.format(card_id))

        return card
    
    @card.doc(security='apikey')
    @card.expect(card_in)
    @card.marshal_with(card_out,envelope='data')
    @card.response(400, 'Invalid Card Details')
    @card.response(404, 'Card Not Found')
    @card.response(500, 'Internal Server Error')
    @authorized
    def put(self,user,session,deck_id,card_id):
        data = request.get_json()
        errors = CardSchema(only=('back','front')).validate(data)
        if errors: raise InvalidDetailsException(errors)

        back = data.get('back')
        front = data.get('front')
        card = session.query(Card).filter_by(user_id=user.id,deck_id=deck_id,id=card_id).first()

        if not card: raise NotFoundException('Card {}'.format(card_id))

        card.front = front
        card.back = back

        session.expire_on_commit=False
        session.commit()

        return card
    
    @card.doc(security='apikey')
    @card.response(204, 'Deck deleted')
    @card.response(404, 'Deck Not Found')
    @card.response(500,'Internal Server Error') 
    @authorized
    def delete(self,user,session,deck_id,card_id):

        card = session.query(Card).filter_by(user_id=user.id,deck_id=deck_id,card_id=card_id).first()
        
        if not card: raise NotFoundException('Card {}'.format(card_id))

        session.delete(card)
        session.commit()
        session.close()
        return {
            'data':{
                'message': 'Deck with id: {} has been deleted'.format(deck_id)}
            },204



