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
    @tag.marshal_with(deckSwagger.outputModelWithTags,envelope='data')
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
    @tag.marshal_with(deckSwagger.outputModelWithTags,envelope='data')
    @tag.response(400, 'Invalid Details')
    @tag.response(401, 'Unauthorized')
    @tag.response(404, 'Deck Not Found')
    @tag.response(500, 'Internal Server Error')
    @authorized
    def put(self,user,session,deck_id):

        data = request.get_json()
        errors = TagListSchema().validate(data)
        if errors: raise InvalidDetailsException(errors)

        deck = session.query(Deck).filter_by(user_id=user.id,id=deck_id).first()
        if not deck: raise NotFoundException('Deck {}'.format(deck_id))

        tag_ids = data.get('tags')
        tags = session.query(Tag).filter(Tag.id.in_(tag_ids)).all()

        tags_ids_current = [tag.id for tag in tags]

        #? Checking if tag ids are valid 
        if len(tag_ids) != len(tags): 
            diff = set(tag_ids).difference(set(tags_ids_current))
            raise NotFoundException('Tags with id {}'.format(diff))

        deck.tags = []
        deck.tags.extend(tags)
        session.expire_on_commit = False
        session.commit()

        return deck


        


