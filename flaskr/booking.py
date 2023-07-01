from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from flaskr.auth import login_required
from flaskr.db import get_db

import folium
import json
from flask import jsonify
# Hi melv


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