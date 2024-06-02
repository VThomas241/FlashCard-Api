from app.core.models import Card,Deck

def test_no_cards(client,session,user_details):
    res = client.get('/decks/1',headers=user_details['headers'])

    assert len(res.json['data']['cards']) == 0

    cards = session.query(Deck).filter_by(id=1,user_id=1).first().cards

    assert len(cards) == 0

def test_card_creation_invalid_details(client,session,user_details):
     # <-------- Missing input -------->
    res = client.post('/decks/1/cards/',headers={
        'Authorization': 'Bearer ' + user_details['token']
    },
    json=dict())

    assert res.status_code == 400

    # <-------- Missing Bearer prefix -------->
    res = client.post('/decks/1/cards/',headers={
        'Authorization': user_details['token']
    },
    json=dict(front='front',back='back'))

    assert res.status_code == 401

    # <-------- Missing Token -------->
    res = client.post('/decks/1/cards/',
    json=dict(front='front',back='back'))

    assert res.status_code == 401

    card = session.query(Card).first()
    assert not card

def test_card_creation(client,session,user_details):
    res = client.post('/decks/1/cards/',json=dict(front='front',back='back'),headers=user_details['headers'])
    assert res.status_code == 201

    card = res.json['data']

    assert card
    assert card['id'] == 1
    assert card['deck_id'] == 1
    assert card['front'] == 'front'
    assert card['back'] == 'back'
    assert card['status'] == 'new'

    card = session.query(Card).filter_by(id=1,deck_id=1,front='front',back='back',status='new')
    assert card

def test_card_creation_duplicate(client,session,user_details):
    card = session.query(Card).filter_by(id=1,deck_id=1,front='front',back='back',status='new')
    assert card

    res = client.post('/decks/1/cards/',json=dict(front='front',back='back'),headers=user_details['headers'])
    assert res.status_code == 400


def test_card_get(client,session,user_details):
    res = client.get('decks/1/cards/1',headers=user_details['headers'])
    assert res.json['data']

# implement crad update invalid details and for decks too

def test_card_update_details(client,session,user_details):
    res = client.put('decks/1/cards/1',json=dict(front='front_changed',back='back_changed'),headers=user_details['headers'])
    assert res.status_code == 200

    card = res.json['data']

    assert card
    assert card['id'] == 1
    assert card['deck_id'] == 1
    assert card['front'] == 'front_changed'
    assert card['back'] == 'back_changed'

    card = session.query(Card).filter_by(id=1,deck_id=1,front='front_changed',back='back_changed')
    assert card
