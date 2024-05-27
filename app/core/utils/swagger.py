from flask_restx import fields, Model
from app.core.utils.exceptions import InvalidFilterField

# from abc import ABC

class SwaggerModel(Model):

    models: list[Model] = []

    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.models.append(self)

    # def filter(self, name:str, fields: tuple[str]|str|None = None) -> Model:
    #     '''
    #     Filters the required fields from the Swagger Model
    #     :param str name: The name of the new model.
    #     :param tuple fields: The fields from the model you want to keep.
        
    #     '''

    #     for model in self.models:
    #         if model.name == name: return model

    #     if not fields: return
    #     if type(fields) == str: fields = (fields,)

    #     fields_to_clone = {}
    #     for field in fields:
    #         if field not in self.keys(): raise InvalidFilterField(field)
    #         fields_to_clone[field] = self.get(field)

    #     new_model = SwaggerModel.clone(name,fields_to_clone)
    #     return new_model

class cardSwagger:
    inputModel = SwaggerModel(
        'Card Input',
        {
            'front': fields.String(required=True, description='Card Front'),
            'back': fields.String(required=True, description='Card Back')
        })

    outputModel = SwaggerModel(
        'Card Output',
        {
            'id': fields.Integer(required=True, description='The card ID'),
            'deck_id': fields.Integer(required=True, description='The deck ID'),
            'front': fields.String(required=True, description='Card Front'),
            'back': fields.String(required=True, description='Card Back'),
            'status': fields.String(required=True,description='Card Status')
        })
    

class deckSwagger:
    __tag_model = SwaggerModel(
        'temp tag model',
        {
            'id': fields.Integer(required=True, description='Tag ID'),
            'name': fields.String(required=True, description='Tag name'),
        }
    )

    inputModel = SwaggerModel(
        'Deck Input',
        {
            'name': fields.String(required=True, description='Deck Name'),
        })

    outputModel = SwaggerModel(
        'Deck Output',
        {
            'id': fields.Integer(required=True, description='Deck ID'),
            'name': fields.String(required=True, description='Deck Name'),
            'new': fields.Integer(required=True, description='Cards that are new'),
            'learning': fields.Integer(required=True, description='Cards that are being learnt'),
            'review': fields.Integer(required=True, description='Cards to be reviewed'),
            'tags': fields.Nested(__tag_model,as_list=True)
        })
    
   
    outputModelWithTags = SwaggerModel(
        'Deck Output With Tags',
        {
            'id': fields.Integer(required=True, description='Deck ID'),
            'name': fields.String(required=True, description='Deck Name'),
            'tags': fields.Nested(__tag_model,as_list=True)
        }
    )

    outputModelWithCards = outputModel.inherit(
        'Deck Output With Cards',
        {
            'cards': fields.Nested(cardSwagger.outputModel,as_list=True)
        }
    )

class tagSwagger:
    inputModel = SwaggerModel(
    'Tag Input',
    {
        'name': fields.String(required=True, description='Tag name'),
        'color': fields.String(description='Tag color')
    }
    )
    outputModel = SwaggerModel(
    'Tag Output',
    {
        'id': fields.Integer(required=True, description='Tag ID'),
        'name': fields.String(required=True, description='Tag name'),
        'color': fields.String(required=True, description='Tag color')
    }
    )

    outputModelWithDecks = outputModel.inherit(
    'Tag Output With Decks',
    {
        'decks': fields.Nested(deckSwagger.outputModelWithTags,as_list=True)
    }
    )
    
    outputList = SwaggerModel(
    'Tag Ids',
    {
        'tags': fields.List(fields.Integer,required=True,description='Tag ids')
    }
    )




class errorSwagger:
    model = SwaggerModel(
    'Error',
    {
        "code": fields.Integer("Error code"),
        "name": fields.String("Error Name"),
        "description": fields.String("Error Message"),
    })

class loginSwagger:
    model = SwaggerModel(
    'Login',
    {
        'email': fields.String(required=True, default='vivek@gmail.com', description='Your user email'),
        'password': fields.String(required=True, default='password',description='Your account password')
    })

class registerSwagger:
    model = SwaggerModel(
    'Registration',
    {
        'user_name': fields.String(required=True, description="Your user name"),
        'email': fields.String(required=True, description="Your email"),
        'password': fields.String(required=True, description="Your password"),
    })

class tokenSwagger:
    model = SwaggerModel(
    'Token',
    {
    'token': fields.String(required=True, description='Your user email')
    })



class reviewSwagger:
    model = SwaggerModel(
    'Review',
    {
        'cards': fields.Nested(cardSwagger.outputModel,as_list=True)
    }
)