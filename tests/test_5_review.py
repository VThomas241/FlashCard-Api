from app.core.models import Deck,Card,User,Review

def test_review(client,session,user_details):
    session.expire_on_commit = False

    user = session.get(User,1)
    deck = Deck(name='review_test')
    user.decks.append(deck)

    session.commit()

    card_1 = Card(user_id=user.id,deck_id=deck.id,front='reviewf_1',back='reviewb_1')
    card_2 = Card(user_id=user.id,deck_id=deck.id,front='reviewf_2',back='reviewb_2')
    card_3 = Card(user_id=user.id,deck_id=deck.id,front='reviewf_3',back='reviewb_3')
    card_4 = Card(user_id=user.id,deck_id=deck.id,front='reviewf_4',back='reviewb_4')
    card_5 = Card(user_id=user.id,deck_id=deck.id,front='reviewf_5',back='reviewb_5')
    card_6 = Card(user_id=user.id,deck_id=deck.id,front='reviewf_6',back='reviewb_6')

    cards = [card_1,card_2,card_3,card_4,card_5,card_6]
    session.add_all(cards)

    session.commit()

    assert len(session.query(Card).filter_by(user_id=user.id,deck_id=deck.id).all()) == 6

    for card in cards: assert card.status == 'new'

    res = client.post(f'/decks/{deck.id}/review',json=dict(cards=[
        {'id': card_1.id,'status': 'learning'},
        {'id': card_2.id,'status': 'learning'},
        {'id': card_3.id,'status': 'review'},
        {'id': card_4.id,'status': 'learning'},
    ]),headers=user_details['headers'])

    print(res.json)
    assert res.status_code == 200

    reviews = session.query(Review).all()
    assert len(reviews) != 0
    review = reviews[0]
    assert review.user_id == 1
    assert review.deck_id == deck.id
    assert review.deck_name == deck.name



