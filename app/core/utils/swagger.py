from flask_restx import fields,Model

error_fields = Model(
    'Error',
    {
        "code": fields.Integer("Error code"),
        "name": fields.String("Error Name"),
        "description": fields.String("Error Message"),
    })

login_details = Model(
    'Login',
    {
        'email': fields.String(required=True, default='vivek@gmail.com', description='Your user email'),
        'password': fields.String(required=True, default='password',description='Your account password')
    })

token = Model(
    'Token',
    {
    'token': fields.String(required=True, description='Your user email')
    })

card_in = Model(
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

card_status = Model(
    'Card Status',
    {
        'id': fields.Integer(required=True, description='The Card ID'),
        'status': fields.String(required=True, description='The Card Status')
    }
)
deck_in = Model(
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


deck_deleted = Model(
    'Deck Deleted',
    {
        'message': fields.String(required=True, description='Deck with id: 1 has been deleted')
    }
)

tag_ids = Model(
    'Tag Ids',
    {
        'tags': fields.List(fields.Integer,required=True,description='Tag ids')
    }
)

tag_id = Model(
    'Tag Id only',
    {
        'id': fields.Integer(required=True, description='Tag ID'),
    }
)
tag_name = Model(
    'Tag Name only',
    {
        'name': fields.String(required=True, description='Tag name')
    }
)
tag_id_name = Model(
    'Tag Id and Name',
    {
        'id': fields.Integer(required=True, description='Tag ID'),
        'name': fields.String(required=True, description='Tag name')
    })

tag_decks = tag_id_name.inherit(
    'Tag full details',
    {
        'decks': fields.Nested(deck_out,as_list=True)
    }    
)

deck_out_tags = deck_out.inherit(
    'Deck Tags',
    {
        'tags': fields.Nested(tag_id_name,as_list=True)
    }
)

review = Model(
    'Review',
    {
        'cards': fields.Nested(card_status,as_list=True)
    }
)
# tag_id_name = Model(
#     'Tag Id only',
#     {
#         'id': fields.Integer(required=True, description='Tag ID')
#     }
# )

model_list = (
    error_fields, login_details, token,
    deck_in, deck_out, deck_out_cards, deck_deleted, deck_out_tags,
    card_in, card_out, card_status,
    tag_id, tag_ids, tag_name, tag_id_name, tag_decks
)
