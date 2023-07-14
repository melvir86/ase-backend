import pytest
import sqlite3
from flaskr import create_app
import warnings
import json
import requests

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def client(app):
    return app.test_client()


#Test create card Api.

def test_createCard(client):
    
    payload = {
        'uid' : 6,
        'name' : 'test',
        'number' : '12345',
        'expiry_month': 'June',
        'expiry_year': '2029',
        'cve': '123',
        'description': 'Bla bla',
        'status': 'Active'
    }

    #Send a POST request to the createCard endpoint with the payload

    response = client.post('/api/createCard', json=payload)

    #Check that the response status code is 201 (OK)

    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    
    

    #Check that the card was inserted into the database

    card = json.loads(response.get_data(as_text=True))
    #print("Card response")
    

    assert b'success' in response.data


def test_listCard(client):
    #Prepare a JSON payload for the request

    #Send a POST request to the listCard endpoint with the payload

    response = client.post('/api/listCard?uid=6')

    #Check that the response status code is 200 (OK)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

   

    #Check that the card was inserted into the database
    
    card = json.loads(response.get_data(as_text=True))
    

    assert card is not None
    assert card[0]["status"] == 'Active'
    assert card[0]["user_id"] == 6
    assert card[0]["cve"] =='123'

def test_getCard(client):
    #Prepare a JSON payload for the request

    #Send a POST request to the getCard endpoint with the payload

    response = client.post('/api/1/getCard')

    #Check that the response status code is 200 (OK)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

    

    #Check that the card was inserted into the database

    card = json.loads(response.get_data(as_text=True))
    

    assert card is not None
    assert card[0]["status"] == 'Active'
    assert card[0]["user_id"] == 6
    assert card[0]["cve"] =='123'


def test_updateCard(client):
    # Prepare a JSON payload for the request
    #TestUser ID is 6 in schema
   
    payload = {
        'uid' : 6,
        'name' : 'test1',
        'number' : '123456',
        'expiry_month': 'June',
        'expiry_year': '2029',
        'cve': '123',
        'description': 'Bla bla',
        'status': 'Active'
    }
        

    # Send a POST request to the updateCard endpoint with the payload
    
    response = client.post('/api/1/updateCard', json=payload)
    

    #Check that the response status code is 200 (OK)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    
    

    #Check that the card was inserted into the database

    card = json.loads(response.get_data(as_text=True))
    

    assert b'success' in response.data



def test_deleteCard(client):
    
    
    #Send a POST request to the deleteCard endpoint with the payload

    response = client.post('/api/1/deleteCard')

    #Check that the response status code is 200 (OK)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    
   
    #Check that the card was inserted into the database

    card = json.loads(response.get_data(as_text=True))
    #print("Card response")
    

    assert b'success' in response.data

   
    