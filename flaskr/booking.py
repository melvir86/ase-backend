from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from flaskr.auth import login_required
from flaskr.db import get_db

import folium
import json
from flask import jsonify
from flaskr.db import get_db


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

@bp.route('/api/bookcar', methods=('GET', 'POST'))
def bookcar():
    db = get_db()
    try:
        db = get_db()

        source = request.json['source']
        destination = request.json['destination']

        # Fetch an available car for booking
        booking = db.execute("SELECT * FROM booking WHERE status = 'available' ORDER BY RANDOM() LIMIT 1").fetchone()

        if booking is None:
            return jsonify({'success': False, 'message': 'No available car for you ....!'})

        car_id = booking['car_id']

        # Update booking status, source, and destination
        db.execute("UPDATE booking SET status = 'booked', source = ?, destination = ? WHERE car_id = ?", (source, destination, car_id))
        db.commit()

        # Get the updated booking 
        updated_booking = db.execute("SELECT * FROM booking WHERE id = ?", (booking['id'],)).fetchone()

        # Convert the row object to a dictionary
        updated_booking_dictionary = dict(updated_booking)

        # Update the values 
        updated_booking_dictionary['source'] = source
        updated_booking_dictionary['destination'] = destination
        updated_booking_dictionary['status'] = 'booked'

        return jsonify({'success': True, 'message': 'Car booked and waiting for acceptance by the driver', 'booking': updated_booking_dict})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Booking failed.Sorry !', 'error': str(e)})