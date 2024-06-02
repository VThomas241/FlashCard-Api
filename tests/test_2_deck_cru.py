from app.core.models import Deck,Card
from sqlalchemy import select

deck_name = 'new_deck'

def test_deck_empty(client,session,user_details):
    res = client.get('/decks/',headers=user_details['headers'])
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



def test_deck_creation(client,session,user_details):
    res = client.post('/decks/',headers=user_details['headers'],json=dict(name=deck_name))
    assert res.status_code == 201
    deck = res.json['data']

    assert deck
    assert deck['id'] == 1
    assert deck['name'] == deck_name
    assert deck['new'] == 0
    assert deck['learning'] == 0
    assert deck['review'] == 0
    assert len(deck['tags']) == 0

    deck = session.execute(select(Deck).filter_by(name=deck_name,user_id=1)).first()
    assert deck

def test_deck_creation_duplicate(client,session,user_details):
    
    deck = session.execute(select(Deck).filter_by(name=deck_name)).first()
    assert deck

    res = client.post('/decks/',headers=user_details['headers'],json=dict(name=deck_name))

    assert res.status_code == 400

def test_get_decks(client,session,user_details):
    res = client.get('/decks/',headers=user_details['headers'])
    decks = res.json['data']
    assert  len(decks) == 1
    assert decks[0]['id'] == 1
    assert decks[0]['name'] == deck_name
    assert decks[0]['new'] == 0
    assert decks[0]['learning'] == 0
    assert decks[0]['review'] == 0
    assert len(decks[0]['tags']) == 0

def test_deck_cards_and_tags_empty(client,session,user_details):
    res = client.get('/decks/1',headers=user_details['headers'])
    assert len(res.json['data']['cards']) == 0 
    assert len(res.json['data']['tags']) == 0

    deck = session.query(Deck).filter_by(id=1,user_id=1).first()
    cards = deck.cards
    tags = deck.tags
    
    assert len(cards) == 0
    assert len(tags) == 0

def test_deck_update_name(client,session,user_details):
    res = client.put(
        '/decks/1',headers=user_details['headers'],
        json=dict(name='changed_name'))
    

    deck = res.json['data']
    assert deck['id'] == 1
    assert deck['name'] == 'changed_name'

    deck_from_db = session.query(Deck).filter_by(id=1,name='changed_name',user_id=1).first()
    assert deck_from_db.id == 1
    assert deck_from_db.user_id == 1
    assert deck_from_db.name == 'changed_name'