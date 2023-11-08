from flask_restx import Namespace,Resource
from flask import request

from app.core.models import Deck,Card
from app.core.utils.validators import ReviewSchema
from app.core.utils.exceptions import NotFoundException, InvalidDetailsException
from app.core.utils.swagger import deck_out, review
from app.core.utils.protected import authorized

review_NS = Namespace(
    'review',
    'Endpoint to update deck after review',
    path='/decks',
)

@review_NS.route('/<int:deck_id>/review')
class Review(Resource):

    @review_NS.doc(security='apikey')
    @review_NS.expect(review)
    @review_NS.marshal_with(deck_out)
    @review_NS.response(400, 'Invalid Details')
    @review_NS.response(401, 'Unauthorized')
    @review_NS.response(404, 'Deck/Cards Not Found')
    @review_NS.response(500, 'Internal Server Error')
    @authorized
    def post(self,user,session,deck_id):

        statuses = {
            'new' : 0,
            'learning' : 0,
            'review' : 0
        }
        
        data = request.get_json()
        errors = ReviewSchema().validate(data)

        if errors : raise InvalidDetailsException(errors)
        cards = data.get('cards')
        
        deck = session.query(Deck).filter_by(id=deck_id,user_id=user.id).first()
        if not deck: raise NotFoundException('Deck {}'.format(deck_id))

        cards = sorted(cards,key=lambda x: x.get('id'))
        card_ids = [card['id'] for card in cards] 

        db_cards = session.query(Card).filter(
            Card.user_id==user.id,
            Card.deck_id==deck_id,
            Card.id.in_(card_ids)).order_by(Card.id.asc()).all()
        
        db_cards_ids = [card.id for card in db_cards]
        
        if len(card_ids) != len(db_cards): 
            diff = set(card_ids).difference(set(db_cards_ids))
            raise NotFoundException('Cards {}'.format(diff))


# START Check validity of implementation -----------------------------------------------------------------------------------------------

        for idx in len(card_ids):
            if db_cards[idx]['status'] != cards[idx]['status']:
                statuses[db_cards[idx]['status']] -= 1
                statuses[cards[idx]['status']] += 1

                db_cards[idx]['status'] = cards[idx]['status']

        for key in statuses:
            deck[key]+= statuses[key]

# END ----------------------------------------------------------------------------------------------------------------------------------

        session.expire_on_commit = False
        session.commit()

        return deck