from flask_restx import Namespace,Resource
from app.core.models import Card,Deck

from app.core.utils.validators import CardSchema
from app.core.utils.protected import authorized
from app.core.utils.swagger import card_in,card_out
from app.core.utils.exceptions import InvalidDetailsException,NotFoundException

from flask import request

cards = Namespace('cards','Endpoints related to cards',path='/decks')

@cards.route('/<int:deck_id>/card/')
class CardsResource(Resource):
    @cards.doc(security='apikey')
    @cards.expect(card_in)
    @cards.marshal_with(card_out)
    @cards.response(400,'Invalid Card Details')
    @cards.response(404,'Deck Not Found')
    @cards.response(500,'Internal Server Error')
    @authorized
    def post(self,user,session,deck_id):
        deck = session.query(Deck).filter_by(user_id=user.id,deck_id=deck_id).first()

        if not deck: raise NotFoundException('Deck {}'.format(deck_id))

        data = request.get_json()

        errors = CardSchema(only=('back','front')).validate(data)
        if errors: raise InvalidDetailsException(errors)

        back = data.get('back')
        front = data.get('front')

        card = Card(user_id=user.id, deck_id=deck_id, front=front, back=back)
        deck.append(card)
        session.expire_on_commit = False
        session.commit()
        
        return card