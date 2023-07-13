from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from flaskr.auth import login_required
from flaskr.db import get_db

import folium
import json
from flask import jsonify

bp = Blueprint('job', __name__)
#List all the jobs function.

@bp.route('/api/listJob', methods=('GET', 'POST'))
def listJob():
    uid = request.args.get('uid')
#Getting data from the booking table and car table referencing each other on same key uid.

    db = get_db()
    jobs = db.execute(
        'SELECT *'
        ' FROM booking b JOIN car c ON b.car_id = c.id'
        ' WHERE c.user_id = ?',
        (uid,)
    ).fetchall()

    return json.dumps([dict(ix) for ix in jobs], indent=4, sort_keys=True, default=str)