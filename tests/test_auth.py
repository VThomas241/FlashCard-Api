from app.core.models import User

def test_create_user_invalid_details(client,user_details):
    # Blank input
    response = client.post('/register/',json=dict(
        user_name='',
        email= user_details['email'],
        password= user_details['password']
    ))
    assert response.status_code == 400
    
    # Missing input
    response = client.post('/register/',json=dict(
        email= user_details['email'],
        password= user_details['password']
    ))
    assert response.status_code == 400


def test_create_user(client,Session,user_details):
    with Session() as session:
        assert session.query(User).first() == None
        response = client.post('/register/',json=dict(
            user_name='vivek24',
            email= user_details['email'],
            password= user_details['password']
        ))
        assert response.status_code == 201
        assert session.query(User).first() != None

def test_create_user_duplicate(client,user_details):
    response = client.post('/register/',json=dict(
        user_name='vivek24',
        email= user_details['email'],
        password= user_details['password']
    ))
    assert response.status_code == 403

def test_login_invalid_details(client,user_details):
    response = client.post('/login/',json=dict(
        email= user_details['email'],
        password= ''
    ))
    assert response.status_code == 400

    response = client.post('/login/',json=dict(
        password= user_details['password']
    ))
    assert response.status_code == 400

    response = client.post('/login/',json=dict(
        email= user_details['email']+'incorrect',
        password= user_details['password']
    ))
    assert response.status_code == 404
    

def test_login_valid_details(client,user_details):
    response = client.post('/login/',json=dict(
        email= user_details['email'],
        password= user_details['password']
    ))
    print(response.json)
    assert response.status_code == 200
    assert response.json['data']['token']