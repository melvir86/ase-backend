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




def test_createFeedback(client):
    #Prepare a JSON payload for the request
    #TestUser ID is 6 in schema
    payload = {
        'uid': 6,
        'description': 'This is a desc.',
        'feedback': 'Very nice ride'
    }

    #Send a POST request to the createFeedback endpoint with the payload

    response = client.post('/api/createFeedback', json=payload)

    #Check that the response status code is 201 (OK)

    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    
    

    #CCheck that the Feedback was inserted into the database

    feedback = json.loads(response.get_data(as_text=True))
    
    #print(feedback)

    assert b'success' in response.data

def test_listFeedback(client):
    # Prepare a JSON payload for the request

    # Send a POST request to the listFeedback endpoint with the payload

    response = client.post('/api/listFeedback?uid=6')

    # Check that the response status code is 200 (OK)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

    # Add additional assertions to validate the response data or behavior

    # Check that the feedback was inserted into the database

    feedback = json.loads(response.get_data(as_text=True))
    

    assert feedback is not None
    assert feedback[0]["description"] == 'This is a desc.'
    assert feedback[0]["user_id"] == 6
    assert feedback[0]["feedback"] == 'Very nice ride'

def test_listAllFeedback(client):
    # Prepare a JSON payload for the request

    #Send a POST request to the listallFeedback endpoint with the payload

    response = client.post('/api/listAllFeedback')

    #Check that the response status code is 200 (OK)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

    # Add additional assertions to validate the response data or behavior

    #Check that the feedback was inserted into the database

    feedback = json.loads(response.get_data(as_text=True))
    

    assert feedback is not None
    assert feedback[0]["description"] == 'This is a desc.'
    assert feedback[0]["user_id"] == 6
    assert feedback[0]["feedback"] == 'Very nice ride'



def test_getFeedback(client):
    # Prepare a JSON payload for the request

    #Send a POST request to the getFeedback endpoint with the payload

    response = client.post('/api/1/getFeedback')

    #Check that the response status code is 200 (OK)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

    # Add additional assertions to validate the response data or behavior

    #Check that the feedback was inserted into the database

    feedback = json.loads(response.get_data(as_text=True))
    

    assert feedback is not None
    assert feedback[0]["description"] == 'This is a desc.'
    assert feedback[0]["user_id"] == 6
    assert feedback[0]["feedback"] == 'Very nice ride'



def test_updateCard(client):
    # Prepare a JSON payload for the request
    #TestUser ID is 6 in schema
   
    payload = {
        'uid': 6,
        'description': 'This is a description.',
        'feedback_info': 'Very nice ridee'
    }
        

    #Send a POST request to the update Feedback endpoint with the payload
    
    response = client.post('/api/1/updateFeedback', json=payload)
    

    #Check that the response status code is 200 (OK)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    
    

    #Check that the feedback was inserted into the database

    feedback= json.loads(response.get_data(as_text=True))
    

    assert b'success' in response.data


def test_deleteFeedback(client):
    
    
    #Send a POST request to the deleteFeedback endpoint with the payload

    response = client.post('/api/1/deleteFeedback')

    # Check that the response status code is 200 (OK)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    
    

    #Check that the feedback was inserted into the database

    feedback = json.loads(response.get_data(as_text=True))
    
    

    assert b'success' in response.data



