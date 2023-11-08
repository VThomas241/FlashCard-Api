from flask_restx import fields,Model

class InvalidFilterField(Exception):
    def __init__(self, field, *args: object) -> None:
        self.message = "The model does not contain the field '{}'".format(field)
        super().__init__(self.message,*args)

class SwaggerModel(Model):

    models: list[Model] = []

    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.models.append(self)

    def filter(self,fields:tuple[str] | str | None = None)->Model:
        if not fields: return
        if type(fields) == str: fields = (fields,)
        fields_to_clone = {}
        new_name:str = self.name + '-{'
        for field in fields:
            if field not in self.keys(): raise InvalidFilterField(field)
            fields_to_clone[field] = self.get(field)
            new_name += field + ','

        new_name = new_name.rstrip(',') + '}'
        new_model = SwaggerModel.clone(new_name,fields_to_clone)
        return new_model


def test():
    tag.filter(['id','name'])

error_fields = SwaggerModel(
    'Error',
    {
        "code": fields.Integer("Error code"),
        "name": fields.String("Error Name"),
        "description": fields.String("Error Message"),
    })

login_details = SwaggerModel(
    'Login',
    {
        'email': fields.String(required=True, default='vivek@gmail.com', description='Your user email'),
        'password': fields.String(required=True, default='password',description='Your account password')
    })

token = SwaggerModel(
    'Token',
    {
    'token': fields.String(required=True, description='Your user email')
    })

card_in = SwaggerModel(
    'Card Input',
    {
        'front': fields.String(required=True, description='Card Front'),
        'back': fields.String(required=True, description='Card Back')
    })

card_out = card_in.inherit(
    'Card Output',
    {
        'id': fields.Integer(required=True, description='The card ID'),
        'deck_id': fields.Integer(required=True, description='The deck ID'),
        'status': fields.String(required=True,description='Card Status' )
    })

card_status = SwaggerModel(
    'Card Status',
    {
        'id': fields.Integer(required=True, description='The Card ID'),
        'status': fields.String(required=True, description='The Card Status')
    }
)
deck_in = SwaggerModel(
    'Deck Input',
    {
        'name': fields.String(required=True, description='Deck Name'),
    })

deck_out = deck_in.inherit(
    'Deck Output',
    {
        'id': fields.Integer(required=True, description='Deck ID'),
        'new': fields.String(required=True, description='Cards that are new'),
        'learning': fields.String(required=True, description='Cards that are being learnt'),
        'review': fields.String(required=True, description='Cards to be reviewed')
    })

deck_out_cards = deck_out.inherit(
    'Deck Cards',
    {
        'cards': fields.Nested(card_out,as_list=True)
    }
)


deck_deleted = SwaggerModel(
    'Deck Deleted',
    {
        'message': fields.String(required=True, description='Deck with id: 1 has been deleted')
    }
)

tag_ids = SwaggerModel(
    'Tag Ids',
    {
        'tags': fields.List(fields.Integer,required=True,description='Tag ids')
    }
)

tag = SwaggerModel(
    'Tag',
    {
        'id': fields.Integer(required=True, description='Tag ID'),
        'name': fields.String(required=True, description='Tag name'),
        'decks': fields.Nested(deck_out,as_list=True)
    }
)


deck_out_tags = deck_out.inherit(
    'Deck Tags',
    {
        'tags': fields.Nested(tag.filter(('id','name')),as_list=True)
    }
)

review = SwaggerModel(
    'Review',
    {
        'cards': fields.Nested(card_status,as_list=True)
    }
)

if __name__ == '__main__':
    test()