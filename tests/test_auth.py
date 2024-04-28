import pytest
from app import create_app
from app.config import TestingConfig
from flask import json

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            pass
        yield client

########### REGISTER ############
def test_register_user(client):
    """Test user registration."""
    response = client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['user'] == "user registered"
    assert 'token' in data

def test_register_user_with_existing_email(client):
    """Test user registration should fail if the email already exists."""

    existing_user = {'username': 'existinguser', 'email': 'test@example.com', 'password': 'password123'}
    client.post('/auth/register', json=existing_user)


    response = client.post('/auth/register', json={
        'username': 'newtestuser',
        'email': 'test@example.com',  
        'password': 'newpassword123'
    })
    assert response.status_code == 409  
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == "Email already in use"  


############# LOGIN #############
def test_register_user_fail_missing_data(client):
    """Test registration failure due to missing data."""
    response = client.post('/auth/register', json={
        'username': 'testuser2'
    })
    assert response.status_code == 400

def test_login_user(client):
    """Test successful login after registration."""
  
    client.post('/auth/register', json={
        'username': 'testlogin',
        'email': 'login@example.com',
        'password': 'loginpassword'
    })
 
    response = client.post('/auth/login', json={
        'email': 'login@example.com',
        'password': 'loginpassword'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Login successful'
    assert 'token' in data

def test_login_user_fail(client):
    """Test login failure with incorrect credentials."""
    response = client.post('/auth/login', json={
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 404
