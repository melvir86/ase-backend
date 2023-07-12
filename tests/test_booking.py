import pytest
import sqlite3
from flaskr import create_app
from flaskr.db import get_db
import warnings
import json

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    with app.app_context():
        db = get_db()
        yield db

def test_show_cars_success(client):
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    response = client.get('/api/showCars')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    # Add additional assertions to validate the response data
    assert b'Mazda' in response.data
    assert b'6' in response.data
    assert b'Mazda' in response.data
    assert b'3 Hb' in response.data

def test_bookcar(client, db):
    # Prepare a JSON payload for the request
    payload = {
        'uid': 1,
        'source': 'Location X',
        'destination': 'Location Y'
    }

    # Send a POST request to the bookcar endpoint with the payload
    response = client.post('/api/bookcar', json=payload)

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

    # Add additional assertions to validate the response data or behavior

    # Check that the booking was inserted into the database
    booking = db.execute('SELECT * FROM booking ORDER BY created DESC LIMIT 1').fetchone()
    assert booking is not None
    assert booking['user_id'] == 1
    assert booking['source'] == 'Location X'
    assert booking['destination'] == 'Location Y'
    assert float(booking['cost']) == 12.5
    assert booking['status'] == 'Booked'


def test_list_requests(client, db):
    # Insert some test data into the booking table
    db.execute(
        'INSERT INTO booking (user_id, source, destination, cost, status)'
        ' VALUES (?, ?, ?, ?, ?)',
        (1, 'Location X ', 'Location Y', 12.50, 'Booked')
    )
   
   

    # Send a GET request to the listRequests endpoint
    response = client.get('/api/listRequests')

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Check that the response has the correct content type
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

    # Convert the response data from JSON to a Python list of dictionaries
    requests = json.loads(response.data)

    

    # Assert specific request information
    assert requests[0]['user_id'] == 1
    assert requests[0]['source'] == 'Location X'
    assert requests[0]['destination'] == 'Location Y'
    assert float(requests[0]['cost']) == 12.50
    assert requests[0]['status'] == 'Booked'


   



def test_check_booking(client,db):
   
        # Perform a GET request to the checkBooking endpoint with uid parameter
        response = client.get('/api/checkBooking?uid=1')
        
        # Check the response status code
        assert response.status_code == 200
        
        # Parse the response data from JSON to a Python list of dictionaries
        bookings = json.loads(response.data)
        assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
        
        # Assert the expected booking details
        
        assert bookings[0]['user_id'] == 1
        assert bookings[0]['source'] == 'Location X'
        assert bookings[0]['destination'] == 'Location Y'
        assert float(bookings[0]['cost']) == 12.50
        assert bookings[0]['status'] == 'Booked'



def test_accept_job(client, db):
    # Insert a test record into the booking table
    db.execute(
        'INSERT INTO booking (id, user_id, source, destination, cost, status)'
        ' VALUES (?, ?, ?, ?, ?, ?)',
        (7, 1, 'Location A', 'Location B', 12.50, 'Booked')
    )
    db.commit()

    # Perform a POST request to the acceptJob endpoint with carid parameter
    response = client.post('/api/7/acceptJob?carid=123')

    # Check the response status code
    assert response.status_code == 200

    # Check the response data
    data = json.loads(response.data)
    assert data['success'] == True

    # Verify that the record in the booking table is updated correctly
    booking = db.execute('SELECT * FROM booking WHERE id = 7').fetchone()
    assert booking['status'] == 'Accepted by Driver'
    assert booking['car_id'] == 123

    db.execute('DELETE FROM booking WHERE id = 8')
    db.execute('DELETE FROM booking WHERE user_id = 1')
    db.commit()




