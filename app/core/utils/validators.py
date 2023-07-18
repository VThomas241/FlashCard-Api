from marshmallow import Schema,fields,ValidationError

def empty(value):
    if value.strip() == '': 
        raise ValidationError('Name must not be empty')

def status(value):
    if value.strip() not in ('new','learning','review'): 
        raise ValidationError('Invalid card status')

class LoginSchema(Schema):
    email = fields.String(required=True,validate=empty)
    password = fields.String(required=True,validate=empty)

class RegisterSchema(Schema):
    user_name = fields.String(required=True,validate=empty)
    email = fields.String(required=True,validate=empty)
    password = fields.String(required=True,validate=empty)

class CardSchema(Schema):
    id = fields.Integer(required=True,strict=True)
    status = fields.String(required=True,validate=status)
    back = fields.String(required=True,validate=empty)
    front = fields.String(required=True,validate=empty) 

class DeckSchema(Schema):
    name = fields.String(required=True,validate=empty) 

class ReviewSchema(Schema):
    cards = fields.Nested(CardSchema,only=('id','status'),many=True,required=True)

class TagSchema(Schema):
    id = fields.Integer(required=True,strict=True)
    name = fields.String(required=True,validate=empty) 

class TagListSchema(Schema):
    tags = fields.List(
        fields.Integer(required=True,strict=True),required=True,
        error_messages={'required': 'tags is mandatory field.'}
    )

