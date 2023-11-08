from flask_restx import Namespace,Resource
from flask import request

from app.core.models import Tag
from app.core.utils.exceptions import InvalidDetailsException , NotFoundException
from app.core.utils.swagger import tag
from app.core.utils.validators import TagSchema
from app.core.utils.protected import authorized


tags = Namespace(
    'tag',
    'Endpoint to update deck tags',
    path='/tags'
)



@tags.route('/')
class TagsResource(Resource):
    @tags.doc(security='apikey')
    @tags.doc(params={'id': 'Tag ID'})
    @tags.marshal_with(tag.filter(('decks')))
    @tags.response(400, 'Invalid Details')
    @tags.response(401, 'Unauthorized')
    @tags.response(404, 'Tag Not Found')
    @tags.response(500, 'Internal Server Error')
    @authorized
    def get(self,user,session):

        errors = TagSchema(only=('id')).validate(request.args)
        if errors : raise InvalidDetailsException(errors)

        tag_id = request.args.get('id')
        tag = session.query(Tag).filter_by(id=tag_id,user_id=user.id).first()

        if not tag: raise NotFoundException('Tag {}'.format(tag_id))
        tag.decks
        return tag
    
    @tags.doc(security='apikey')
    @tags.expect(tag.filter(('name')))
    @tags.marshal_with(tag.filter(('id','name')))
    @tags.response(400, 'Invalid Details')
    @tags.response(401, 'Unauthorized')
    @tags.response(500, 'Internal Server Error')
    @authorized
    def post(self,user,session):
        data = request.get_json()

        errors = TagSchema(only=('name')).validate(data)
        if errors: raise InvalidDetailsException(errors)
        
        tag_name = data.get('name')

        tag = Tag(name=tag_name)
        session.add(tag)
        session.expire_on_commit = False
        session.commit()

        return tag

    @tags.doc(security='apikey')
    @tags.expect(tag.filter(('id','name')))
    @tags.marshal_with(tag.filter(('id','name')))
    @tags.response(400, 'Invalid Details')
    @tags.response(401, 'Unauthorized')
    @tags.response(404, 'Tag Not Found')
    @tags.response(500, 'Internal Server Error')
    @authorized
    def put(self,user,session):
        data = request.get_json()
        errors = TagSchema().validate(data=data)

        if errors: raise InvalidDetailsException(errors)
        
        tag = session.query(Tag).filter_by(id=data.get('id'),user_id=user.id).first()
        if not tag: raise NotFoundException('Tag {}'.format(data.get('id')))

        tag.name = data.get('name')
        session.commit()

        return 'Tag {} name changed to {}'.format(data.get('id'),data.get('name'))
    
    @tags.doc(security='apikey')
    @tags.expect(tag.filter(('id')))
    @tags.response(400, 'Invalid Details')
    @tags.response(401, 'Unauthorized')
    @tags.response(404, 'Tag Not Found')
    @tags.response(500, 'Internal Server Error')
    @authorized
    def delete(self,user,session):
        data = request.get_json()
        errors = TagSchema(only=('id')).validate(data=data)

        if errors: raise InvalidDetailsException(errors)

        tag = session.query(Tag).filter_by(id=data.get('id'),user_id=user.id).first()
        if not tag: raise NotFoundException('Tag {}'.format(data.get('id')))

        tag_id = tag.id
        tag_name = tag.name

        session.delete(tag)
        session.commit()

        return "tag ({},{}) deleted".format(tag_id,tag_name),204