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

@bp.route('/api/bookcar', methods=('GET', 'POST'))
def bookcar():
    db = get_db()
    try:
        source = request.json['source']
        destination = request.json['destination']
        
        # Fetch an available car for booking
        
        car_id=db.execute("SELECT car_id FROM booking WHERE status = 'available' LIMIT 1").fetchone()[0]
        
        # Update car status, source, and destination
        db.execute("UPDATE booking SET status = 'booked', source = ?, destination = ? WHERE car_id = ?", (source, destination, car_id))
        db.commit()
        
        booking = db.execute("SELECT * FROM booking WHERE car_id = ?", (car_id,)).fetchone()

        return jsonify({'success': True, 'message': 'Car booked and waiting for accepting', 'booking': dict(booking)})
    except Exception as e:
         return jsonify({'success': False, 'message': 'Booking failed', 'error': str(e)})