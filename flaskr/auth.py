from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from flaskr.auth import login_required
from flaskr.db import get_db

import folium
import json
from flask import jsonify

import functools

import hashlib

bp = Blueprint('auth', __name__)

@bp.route('/api/register', methods=('GET', 'POST'))
def register():
    data = request.get_json()

    if request.method == 'POST':
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        error = None

        print("Username is ", username)
        print("Password is ", password)
        print("Role is ", role)

        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not role:
            error = 'Role is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO user (username, password, role) VALUES (?, ?, ?)",
                (username, password_hash, role),
            )
            db.commit()
            return json.dumps({'success':True}), 201, {'ContentType':'application/json'}

@bp.route('/api/login', methods=('GET', 'POST'))
def login():
    data = request.get_json()

    if request.method == 'POST':
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        error = None

        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()

    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE username = ? AND password = ? AND role = ?', (username, password_hash, role)
    ).fetchall()

    return json.dumps([dict(ix) for ix in user], indent=4, sort_keys=True, default=str)

@bp.route('/api/<int:id>/loadUser', methods=('GET', 'POST'))
def loadUser(id):

    user = get_db().execute(
        'SELECT *'
        ' FROM user u'
        ' WHERE u.id = ?',
        (id,)
    ).fetchall()

    if user is None:
        abort(404, f"User id {id} doesn't exist.")

    return json.dumps([dict(ix) for ix in user], indent=4, sort_keys=True, default=str)