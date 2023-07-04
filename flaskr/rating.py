from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from flaskr.auth import login_required
from flaskr.db import get_db

import folium
import json
from flask import jsonify

bp = Blueprint('rating', __name__)

@bp.route('/api/driverRating', methods=('GET', 'POST'))
def driverRating():
    print("Came here")
    uid = request.args.get('uid')
    print("Uid is ", uid)
    db = get_db()
    car = db.execute(
        'SELECT *'
        ' FROM car c'
        ' WHERE c.user_id = ?',
        (uid,)
    ).fetchall()

    return json.dumps([dict(ix) for ix in car], indent=4, sort_keys=True, default=str)