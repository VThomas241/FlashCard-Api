from app.core.models import Deck
from sqlalchemy import select

deck_name = 'new_deck'
headers = None

def test_define_headers(user_details):
    global headers
    assert user_details['headers']
    headers = user_details['headers']

def test_deck_empty(client,session):
    res = client.get('/decks/',headers=headers)
    assert len(res.json['data']) == 0 

    deck = session.execute(select(Deck)).first()
    assert not deck


def test_deck_creation_invalid(client,session,user_details):
    # <-------- Missing input -------->
    res = client.post('/decks/',headers={
        'Authorization': 'Bearer ' + user_details['token']
    },
    json=dict())

    assert res.status_code == 400

    # <-------- Missing Bearer prefix -------->
    res = client.post('/decks/',headers={
        'Authorization': user_details['token']
    },
    json=dict(name=deck_name))

    assert res.status_code == 401

    # <-------- Missing Token -------->
    res = client.post('/decks/',
    json=dict(name=deck_name))

    assert res.status_code == 401

    deck = session.execute(select(Deck)).first()
    assert not deck



def test_deck_creation(client,session):
    res = client.post('/decks/',headers=headers,json=dict(name=deck_name))
    deck = res.json['data']

    assert deck
    assert deck['id'] == 1
    assert deck['name'] == deck_name
    assert deck['new'] == 0
    assert deck['learning'] == 0
    assert deck['review'] == 0
    assert len(deck['tags']) == 0

    deck = session.execute(select(Deck).filter_by(name=deck_name)).first()
    assert deck

def test_deck_creation_duplicate(client,session):
    
    deck = session.execute(select(Deck).filter_by(name=deck_name)).first()
    assert deck

    res = client.post('/decks/',headers=headers,json=dict(name=deck_name))

    assert res.status_code == 400

def test_get_decks(client,session,user_details):
    res = client.get('/decks/',headers=headers)
    decks = res.json['data']
    assert  len(decks) == 1
    assert decks[0]['id'] == 1
    assert decks[0]['name'] == deck_name
    assert decks[0]['new'] == 0
    assert decks[0]['learning'] == 0
    assert decks[0]['review'] == 0
    assert len(decks[0]['tags']) == 0

    