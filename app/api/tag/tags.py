from flask_restx import Namespace,Resource
from flask import request
from sqlalchemy.orm import Session
from app.core.models import Tag,User
from app.utils.exceptions import InvalidDetailsException , NotFoundException
from app.utils.swagger import tagSwagger
from app.utils.validators import TagSchema
from app.utils.protected import authorized

tags = Namespace(
    'tag',
    'Endpoint to update deck tags',
    path='/tags'
)



@tags.route('/')
class TagCreationResource(Resource):
    @tags.doc(security='apikey')
    @tags.response(401, 'Unauthorized')
    @tags.response(500, 'Internal Server Error')
    @tags.marshal_list_with(tagSwagger.outputModel,envelope='data')
    @authorized
    def get(self,user:User,session:Session):
        tags = session.query(Tag).filter_by(user_id=user.id).all()
        return tags

    @tags.doc(security='apikey')
    @tags.expect(tagSwagger.inputModel)
    @tags.marshal_with(tagSwagger.outputModel,envelope='data')
    @tags.response(400, 'Invalid Details')
    @tags.response(401, 'Unauthorized')
    @tags.response(500, 'Internal Server Error')
    @authorized
    def post(self,user:User,session:Session):
        data = request.get_json()

        errors = TagSchema(only=('name','color')).validate(data)
        if errors: raise InvalidDetailsException(errors)
        
        tag_name,tag_color = data.get('name'),data.get('color')
        tag = Tag(name=tag_name,color=tag_color) if tag_color else Tag(name=tag_name)
        user.tags.append(tag)
        # session.add(tag)
        session.expire_on_commit = False
        session.commit()

        return tag,201


@tags.route('/<int:tag_id>')
class TagsResource(Resource):
    @tags.doc(security='apikey')
    @tags.doc(params={'tag_id': 'Tag ID'})
    @tags.marshal_with(tagSwagger.outputModelWithDecks,envelope='data',as_list=True)
    @tags.response(400, 'Invalid Details')
    @tags.response(401, 'Unauthorized')
    @tags.response(404, 'Tag Not Found')
    @tags.response(500, 'Internal Server Error')
    @authorized
    def get(self,user:User,session:Session,tag_id:int):
        tag = session.query(Tag).filter_by(id=tag_id,user_id=user.id).first()
        if not tag: raise NotFoundException('Tag {}'.format(tag_id))
        [deck.tags for deck in tag.decks]
        return tag
    

    @tags.doc(security='apikey')
    @tags.doc(params={'tag_id': 'Tag ID'})
    @tags.expect(tagSwagger.inputModel)
    @tags.marshal_with(tagSwagger.outputModel,envelope='data',code=201)
    @tags.response(400, 'Invalid Details')
    @tags.response(401, 'Unauthorized')
    @tags.response(404, 'Tag Not Found')
    @tags.response(500, 'Internal Server Error')
    @authorized
    def put(self,user:User,session:Session,tag_id:int):
        data = request.get_json()
        #? Name and color parameters are optional and id is received from the path
        #? So no need of data validation
        # data['id'] = tag_id
        # errors = TagSchema(only=('id',)).validate(data=data)
        # if errors: raise InvalidDetailsException(errors)
        keys = data.keys()
        if 'name' not in keys and 'color' not in keys: raise InvalidDetailsException('Either name or color parameter should be included')  
        tag = session.query(Tag).filter_by(id=tag_id,user_id=user.id).first()
        if not tag: raise NotFoundException('Tag {}'.format(tag_id))

        tag.name = data.get('name',tag.name)
        tag.color = data.get('color',tag.color)
        session.expire_on_commit = False
        session.commit()

        return tag
    
    @tags.doc(security='apikey')
    @tags.doc(params={'tag_id': 'Tag ID'})
    @tags.response(400, 'Invalid Details')
    @tags.response(401, 'Unauthorized')
    @tags.response(404, 'Tag Not Found')
    @tags.response(500, 'Internal Server Error')
    @authorized
    def delete(self,user:User,session:Session,tag_id:int):
        tag = session.query(Tag).filter_by(id=tag_id,user_id=user.id).first()
        if not tag: raise NotFoundException('Tag {}'.format(tag_id))

        session.delete(tag)
        session.commit()
        return None,204