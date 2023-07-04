from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from flaskr.auth import login_required
from flaskr.db import get_db

import folium
import json
from flask import jsonify

bp = Blueprint('car', __name__)

@bp.route('/api/listCarDetails', methods=('GET', 'POST'))
def listCarDetails():
    uid = request.args.get('uid')

    db = get_db()
    cars = db.execute(
        'SELECT * FROM car WHERE user_id = ?',
        (uid,)
    ).fetchall()

    return json.dumps([dict(ix) for ix in cars], indent=4, sort_keys=True, default=str)