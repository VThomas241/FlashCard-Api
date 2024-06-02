from flask_restx import Namespace,Resource
from flask import request

from app.core.models import Deck,Card,Review
from app.utils.validators import ReviewSchema
from app.utils.exceptions import NotFoundException, InvalidDetailsException
from app.utils.swagger import reviewSwagger,deckSwagger
from app.utils.protected import authorized

review = Namespace(
    'review',
    'Endpoint to update deck after review',
    path='/decks',
)

@review.route('/<int:deck_id>/review')
class ReviewCreation(Resource):

    @review.doc(security='apikey')
    @review.expect(reviewSwagger)
    @review.marshal_with(deckSwagger.outputModelWithCards,envelope='data')
    @review.response(400, 'Invalid Details')
    @review.response(401, 'Unauthorized')
    @review.response(404, 'Deck/Cards Not Found')
    @review.response(500, 'Internal Server Error')
    @authorized
    def post(self,user,session,deck_id):
        data = request.get_json()
        errors = ReviewSchema().validate(data)

        if errors : raise InvalidDetailsException(errors)
        cards = data.get('cards')
        
        deck:Deck = session.query(Deck).filter_by(id=deck_id,user_id=user.id).first()
        if not deck: raise NotFoundException('Deck {}'.format(deck_id))

        cards = sorted(cards,key=lambda x: x.get('id'))
        card_ids = [card['id'] for card in cards] 
        
        db_cards = session.query(Card).filter(
            Card.user_id==user.id,
            Card.deck_id==deck_id,
            Card.id.in_(card_ids)).order_by(Card.id.asc()).all()
        
        db_cards_ids = [card.id for card in db_cards]
        
        if len(card_ids) != len(db_cards_ids): 
            invalid_card_ids = set(card_ids).difference(set(db_cards_ids))
            raise NotFoundException('Cards {}'.format(invalid_card_ids))

        for idx in range(len(card_ids)): db_cards[idx].status = cards[idx]['status']
            
        review = Review(user_id=user.id,deck_id=deck.id,deck_name=deck.name)
        session.add(review)
        
        session.expire_on_commit = False
        session.commit()

        deck.cards
        deck.tags
        return deck