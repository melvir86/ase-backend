from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from flaskr.auth import login_required
from flaskr.db import get_db

import folium
import json
from flask import jsonify


bp = Blueprint('booking', __name__)


@bp.route('/')
def index():
    return render_template('card/index.html')
#Show cars api from the database of cars table.

@bp.route('/api/showCars', methods=('GET', 'POST'))
def showCars():
    db = get_db()
    try:
        #Select all cars form the car table.

        cars = db.execute(
            'SELECT *'
            ' FROM car'
            ' ORDER BY created DESC'
        ).fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")
#Return them a json repsone ,using a dict.

    return json.dumps([dict(ix) for ix in cars], indent=4, sort_keys=True, default=str)
#Book car api.

@bp.route('/api/bookcar', methods=('GET', 'POST'))
def bookcar():
    db = get_db()
#Getting THE CUSTOMER ID FROM THE PAYLOAD also the source and destination.

    data = request.get_json()
    uid = data.get('uid')
    cost = 12.50
    db = get_db()

    source = request.json['source']
    destination = request.json['destination']
#Inserting values into the booking last entity as who made the booking where it wants to go also set up the status as booked.
    db.execute(
        'INSERT INTO booking (user_id, source, destination, cost, status)'
        ' VALUES (?, ?, ?, ?, ?)',
        (uid, source, destination, cost, 'Booked')
    )
    db.commit()
#Getting the new inserted row values.

    booking = get_db().execute(
        'SELECT *'
        ' FROM booking b'
        ' WHERE b.user_id = ?'
        ' ORDER BY b.created DESC LIMIT 1',
        (uid,)

    ).fetchall()
   
    return json.dumps([dict(ix) for ix in booking], indent=4, sort_keys=True, default=str)
#List the request of bookings with status booked and returnin them as a JSON.  

@bp.route('/api/listRequests', methods=('GET', 'POST'))
def listRequests():
    db = get_db()

    customer_requests = db.execute(
        'SELECT *'
        ' FROM booking b'
        ' WHERE b.status = "Booked"'
        #' ORDER BY created DESC'
    ).fetchall()

    return json.dumps([dict(ix) for ix in customer_requests], indent=4, sort_keys=True, default=str)
#Check the booking api of a exact specific user since we get the user_id.What booking has a customer done.

@bp.route('/api/checkBooking', methods=('GET', 'POST'))
def checkBooking():
    uid = request.args.get('uid')
#Query the booking table with uid value passing from the payload.

    db = get_db()
    bookings = db.execute(
        'SELECT *'
        ' FROM booking b'
        ' WHERE b.user_id = ?'
        ' ORDER BY b.created DESC LIMIT 1',
        (uid,)
    ).fetchall()

    return json.dumps([dict(ix) for ix in bookings], indent=4, sort_keys=True, default=str)
#Accepting the job by the driver and updating the driver car_id into the booking table.

@bp.route('/api/<int:id>/acceptJob', methods=('POST',))
def acceptJob(id):
    car_id = request.args.get('carid')

    db = get_db()
    #db.execute('UPDATE booking SET status = "Booked", car_id = ? WHERE id = ?', (1, id,))

    db.execute('UPDATE booking SET status = "Accepted by Driver", car_id = ? WHERE id = ?', (car_id, id,))
    db.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
#Getting the car id from the driver id.

@bp.route('/api/<int:id>/getCarId', methods=('GET', 'POST',))
def getCarId(id):
    db = get_db()

    car_id = db.execute(
        'SELECT id'
        ' FROM car c'
        ' WHERE c.user_id = ?',
        (id,)
    ).fetchall()

    return json.dumps([dict(ix) for ix in car_id], indent=4, sort_keys=True, default=str)
#Getting the car details from driver id/

@bp.route('/api/<int:id>/getCarDetails', methods=('GET', 'POST',))
def getCarDetails(id):
    db = get_db()

    car = db.execute(
        'SELECT *'
        ' FROM car c'
        ' WHERE c.user_id = ?',
        (id,)
    ).fetchall()

    return json.dumps([dict(ix) for ix in car], indent=4, sort_keys=True, default=str)
#List all the bookings from booking table joining the user and car details.

@bp.route('/api/listBookings', methods=('GET', 'POST'))
def listBookings():
    db = get_db()

    uid = request.args.get('uid')
    db = get_db()
#Get all the data of the booking also user details and car details where the customer_id is unknows but we have it from the payload as uid.
    booking_history = db.execute(
        'SELECT *'
        ' FROM booking b'
        ' JOIN user u ON b.user_id = u.id'
        ' JOIN car c ON b.car_id = c.id'
        ' WHERE b.user_id = ?'
        ' ORDER BY b.created DESC',
        (uid,)
    ).fetchall()

    return json.dumps([dict(ix) for ix in booking_history], indent=4, sort_keys=True, default=str)

#Changing the position of car from its own position to the user initial position

@bp.route('/api/startBooking', methods=('GET', 'POST'))
def startBooking():
    db = get_db()
    # Get source_x and source_y from the payload
    booking_id = request.json.get('booking_id')
    source_x = request.json.get('source_x')
    source_y = request.json.get('source_y')
    car_id = request.json.get('car_id')

    print("Source is ", source_x, source_y)

    # Step 1 - Update booking table status'
    db.execute('UPDATE booking SET status = "Started" WHERE id = ?', (booking_id,))
    db.commit()

    # Step 2 - Update car table pos_x and pos_y'
    db.execute(
        'UPDATE car SET pos_x = ?, pos_y = ? WHERE id = ?',
        (source_x, source_y, car_id,)
    )
    db.commit()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
#Changing the car poisition from the user position to the desired location as destination.

@bp.route('/api/completeBooking', methods=('GET', 'POST'))
def completeBooking():
    db = get_db()
    #Get source_x and source_y from the payload

    booking_id = request.json.get('booking_id')
    destination_x = request.json.get('destination_x')
    destination_y = request.json.get('destination_y')
    car_id = request.json.get('car_id')

    print("Destination is ", destination_x, destination_y)

    # Step 1 - Update booking table status'
    db.execute('UPDATE booking SET status = "Completed" WHERE id = ?', (booking_id,))
    db.commit()

    # Step 2 - Update car table pos_x and pos_y'
    db.execute(
        'UPDATE car SET pos_x = ?, pos_y = ? WHERE id = ?',
        (destination_x, destination_y, car_id,)
    )
    db.commit()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
#Update the drivers rating function.

@bp.route('/api/rateDriver', methods=('GET', 'POST'))
def rateDriver():
    db = get_db()
    # Get source_x and source_y from the payload
    
    car_id = request.json.get('car_id')
    rating = request.json.get('rating')

    print("Booking Id & Rating is is ", car_id, rating)

    # Step 1 - Update booking table status'
    db.execute('UPDATE car SET rating = ? WHERE id = ?', (rating, car_id,))
    db.commit()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}