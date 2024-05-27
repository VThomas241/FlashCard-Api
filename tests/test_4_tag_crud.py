from app.core.models import Deck,Tag

def test_no_tags(client,session,user_details):
    tags = session.query(Tag).all()
    tags_filtered = session.query(Tag).filter_by(user_id=1).all()

    res = client.get('/tags/',headers=user_details['headers'])
    all_user_tags = res.json['data']

    assert len(tags) == 0
    assert len(all_user_tags) == 0

    res = client.get('/tags/decks/1',headers=user_details['headers'])
    deck_1 = res.json['data']
    
    assert deck_1['id'] == 1
    assert len(tags_filtered) == 0
    assert len(deck_1['tags']) == 0


def test_create_tag(client,session,user_details):
    res = client.post('/tags/',json=dict(),headers=user_details['headers'])
    assert res.status_code == 400

    res = client.post('/tags/',json=dict(name='Tag_1'),headers=user_details['headers'])
    assert res.status_code == 201
    data = res.json['data']
    assert data['id'] == 1
    assert data['name'] == 'Tag_1'
    assert data['color'] == '#2550ca'
    
    all_tags = session.query(Tag).all()
    tag = all_tags[0]

    assert len(all_tags) == 1
    assert tag.user_id == 1
    assert tag.id == 1
    assert tag.name == 'Tag_1'
    assert tag.color == '#2550ca'

    client.post('/tags/',json=dict(name='Tag_2'),headers=user_details['headers'])


def test_get_user_tags(client,session,user_details):
    res = client.get('/tags/',headers=user_details['headers'])
    tags = res.json['data']
    assert tags
    assert len(tags) == 2
    
    tag = tags[1]

    assert tag['id']== 2
    assert tag['name'] == 'Tag_2'
    assert tag['color'] == '#2550ca'


def test_get_decks_by_tag_empty(client,session,user_details):
    res = client.get('/tags/1',headers=user_details['headers'])
    data = res.json['data']

    assert len(data['decks']) == 0
    assert data['id'] == 1
    assert data['name'] == 'Tag_1'

def test_update_tag_name_color(client,session,user_details):
    res = client.put('/tags/1',json=dict(color='#2550ca'),headers=user_details['headers'])
    assert res.status_code == 200

    res = client.put('/tags/1',json=dict(name='Tag_1_Changed'),headers=user_details['headers'])
    assert res.status_code == 200

    res = client.put('/tags/1',json=dict(),headers=user_details['headers'])
    assert res.status_code == 400

    res = client.put('/tags/1',json=dict(name='Tag_1_Changed',color='#2550ca'),headers=user_details['headers'])
    assert res.status_code == 200

    data = res.json['data']
    assert data['id'] == 1
    assert data['name'] == 'Tag_1_Changed'

    db_tag = session.get(Tag,1)
    assert db_tag.name == 'Tag_1_Changed'

def test_update_deck_tags(client,session,user_details):
    res = client.put('/tags/decks/2',json=dict(tags=[1,2]),headers=user_details['headers'])
    assert res.status_code == 404

    res = client.put('/tags/decks/1',json=dict(),headers=user_details['headers'])
    assert res.status_code == 400

    res = client.put('/tags/decks/1',json=dict(gibberish=[1,2]),headers=user_details['headers'])
    assert res.status_code == 400

    res = client.put('/tags/decks/1',json=dict(tags=[]),headers=user_details['headers'])
    assert res.status_code == 200

    res = client.put('/tags/decks/1',json=dict(tags=[1,2]),headers=user_details['headers'])
    assert res.status_code == 200

    deck = session.get(Deck,1)
    assert len(deck.tags) == 2
    assert deck.tags[0].name == 'Tag_1_Changed'
    assert deck.tags[1].name == 'Tag_2'


def test_get_decks_by_tag(client,session,user_details):
    res = client.get('/tags/1',headers=user_details['headers'])
    data = res.json['data']

    assert len(data['decks']) == 1
    assert data['id'] == 1
    assert data['name'] == 'Tag_1_Changed'

def test_delete_tags(client,session,user_details):
    res = client.delete('/tags/4',headers=user_details['headers'])
    assert res.status_code == 404
    res = client.delete('/tags/1',headers=user_details['headers'])
    assert res.status_code == 204
    res = client.delete('/tags/2',headers=user_details['headers'])
    assert res.status_code == 204

    deck = session.get(Deck,1)
    assert len(deck.tags) == 0
    tags = session.query(Tag).all()
    assert len(tags) == 0

    # Adding a third tag at the end to check the test database that all tests were executed.
    res = client.post('/tags/',json=dict(name='Tag_3'),headers=user_details['headers'])
    assert res.status_code == 201
    tag_id = res.json['data']['id']

    res = client.put('/tags/decks/1',json=dict(tags=[tag_id]),headers=user_details['headers'])
    assert res.status_code == 200
