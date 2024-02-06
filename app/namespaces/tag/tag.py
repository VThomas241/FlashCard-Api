from flask_restx import Namespace,Resource
from flask import request

from app.core.models import Deck,Tag
from app.core.utils.exceptions import InvalidDetailsException , NotFoundException
from app.core.utils.swagger import deckSwagger,tagSwagger
from app.core.utils.validators import TagListSchema
from app.core.utils.protected import authorized


tag = Namespace(
    'tag',
    'Endpoint to update deck tags',
    path='/tags/decks'
)

@tag.route('/<int:deck_id>')
class TagResource(Resource):
    @tag.doc(security='apikey')
    @tag.marshal_with(deckSwagger.outputModelWithTags)
    @tag.response(400, 'Invalid Details')
    @tag.response(401, 'Unauthorized')
    @tag.response(404, 'Deck Not Found')
    @tag.response(500, 'Internal Server Error')
    @authorized
    def get(self,user,session,deck_id):
        deck = session.query(Deck).filter_by(user_id=user.id,id=deck_id).first()
        if not deck: raise NotFoundException('Deck {}'.format(deck_id))
        
        deck.tags
        return deck

    @tag.doc(security='apikey')
    @tag.expect(tagSwagger.outputList)
    @tag.marshal_with(deckSwagger.outputModelWithCards)
    @tag.response(400, 'Invalid Details')
    @tag.response(401, 'Unauthorized')
    @tag.response(404, 'Deck Not Found')
    @tag.response(500, 'Internal Server Error')
    @authorized
    def put(self,user,session,deck_id):

        data = request.get_json()
        deck = session.query(Deck).filter_by(user_id=user.id,id=deck_id).first()
        if not deck: raise NotFoundException('Deck {}'.format(deck_id))

        errors = TagListSchema().validate(data)
        if errors: raise InvalidDetailsException(errors)

        tags_ids_new = data.get('tags')            
        tags_current = session.query(Tag).filter(Tag.id.in_(tags_ids_new)).all()
        tags_ids_current = [tag.id for tag in tags_current]

        if len(tags_ids_new) != len(tags_current): 
            diff = set(tags_ids_new).difference(set(tags_ids_current))
            raise NotFoundException('Tags {}'.format(diff))

        deck.tags = []
        deck.tags.extend(tags_current)
        session.expire_on_commit = False
        session.commit()

        return deck


        


