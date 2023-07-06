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

@bp.route('/api/showCars', methods=('GET', 'POST'))
def showCars():
    db = get_db()
    try:
        cars = db.execute(
            'SELECT *'
            ' FROM car'
            ' ORDER BY created DESC'
        ).fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")

    return json.dumps([dict(ix) for ix in cars], indent=4, sort_keys=True, default=str)

@bp.route('/api/bookcar', methods=('GET', 'POST'))
def bookcar():
    db = get_db()

    data = request.get_json()
    uid = data.get('uid')
    cost = 12.50
    db = get_db()

    source = request.json['source']
    destination = request.json['destination']

    db.execute(
        'INSERT INTO booking (user_id, source, destination, cost, status)'
        ' VALUES (?, ?, ?, ?, ?)',
        (uid, source, destination, cost, 'Booked')
    )
    db.commit()

    booking = get_db().execute(
        'SELECT *'
        ' FROM booking b'
        ' ORDER BY b.created DESC LIMIT 1'
    ).fetchall()

   
    return json.dumps([dict(ix) for ix in booking], indent=4, sort_keys=True, default=str)
    
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

@bp.route('/api/checkBooking', methods=('GET', 'POST'))
def checkBooking():
    uid = request.args.get('uid')

    db = get_db()
    bookings = db.execute(
        'SELECT *'
        ' FROM booking b'
        ' WHERE b.user_id = ?'
        ' ORDER BY b.created DESC LIMIT 1',
        (uid,)
    ).fetchall()

    return json.dumps([dict(ix) for ix in bookings], indent=4, sort_keys=True, default=str)

@bp.route('/api/<int:id>/acceptJob', methods=('POST',))
def acceptJob(id):
    car_id = request.args.get('carid')

    db = get_db()
    #db.execute('UPDATE booking SET status = "Booked", car_id = ? WHERE id = ?', (1, id,))
    db.execute('UPDATE booking SET status = "Accepted by Driver", car_id = ? WHERE id = ?', (car_id, id,))
    db.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

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

@bp.route('/api/listBookings', methods=('GET', 'POST'))
def listBookings():
    db = get_db()

    uid = request.args.get('uid')
    db = get_db()

    booking_history = db.execute(
        'SELECT *'
        ' FROM booking b'
        ' JOIN user u ON b.user_id = u.id'
        ' WHERE b.user_id = ?'
        ' ORDER BY b.created DESC',
        (uid,)
    ).fetchall()

    return json.dumps([dict(ix) for ix in booking_history], indent=4, sort_keys=True, default=str)


@bp.route('/api/startBooking', methods=('GET', 'POST'))
def startBooking():
    db = get_db()
    # Get source_x and source_y from the payload
    source_x = request.json.get('source_x')
    source_y = request.json.get('source_y')
    
    # Update pos_x and pos_y where status is 'Accepted by Driver'
    db.execute(
        'UPDATE car SET pos_x = ?, pos_y = ? WHERE status = "Accepted by Driver"',
        (source_x, source_y)
    )
    db.commit()

    # Get the updated rows
    updated_rows = db.execute(
        'SELECT * FROM booking WHERE pos_x = ? AND pos_y = ? AND status = "Accepted by Driver"',
        (source_x, source_y)
    ).fetchall()

    # Return the updated rows
    return jsonify(updated_rows), 200