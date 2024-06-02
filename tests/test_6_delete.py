from app.core.models import Deck,Card

def test_card_delete(client,session,user_details):

    res = client.delete('/decks/1/cards/7',headers=user_details['headers'])
    assert res.status_code == 404

    res = client.delete('/decks/5/cards/1',headers=user_details['headers'])
    assert res.status_code == 404

    res = client.delete('/decks/1/cards/1',headers=user_details['headers'])
    assert res.status_code == 204

    card = session.get(Card,1)
    assert card == None
    
def test_deck_delete(client,session,user_details):
    res = client.post('/decks/',headers=user_details['headers'],json=dict(name='to_be_deleted'))
    assert res.status_code == 201
    
    deck_id = res.json['data']['id']

    res = client.post(f'/decks/{deck_id}/cards/',headers=user_details['headers'],json=dict(front='to_be_deleted',back='sup'))
    assert res.status_code == 201

    res = client.post(f'/decks/{deck_id}/cards/',headers=user_details['headers'],json=dict(front='to_be deleted',back='sup'))
    assert res.status_code == 201

    res = client.delete('/decks/87',headers=user_details['headers'])
    assert res.status_code == 404

    res = client.delete(f'/decks/{deck_id}',headers=user_details['headers'])
    assert res.status_code == 204

    res = client.get(f'/decks/{deck_id}',headers=user_details['headers'])
    assert res.status_code == 404

    deck = session.get(Deck,deck_id)
    assert deck == None

    cards = session.query(Card).filter_by(user_id=1,deck_id=deck_id).all()
    assert len(cards) == 0

# def test_user_delete(client,session,user_details):
#     pass


