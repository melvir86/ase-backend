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
#Register api function.

@bp.route('/api/register', methods=('GET', 'POST'))
def register():
    data = request.get_json()
    #Getting the values from posting payload

    if request.method == 'POST':
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        error = None

        print("Username is ", username)
        print("Password is ", password)
        print("Role is ", role)
#Encypt the password into md5.

        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
#Check if any of the textboxes is empty from the form.

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not role:
            error = 'Role is required.'
#Inserting the values into user table.

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
#Log in function api.

@bp.route('/api/login', methods=('GET', 'POST'))
def login():
    data = request.get_json()
#Getting the palyload.

    if request.method == 'POST':
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        error = None

        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
#Execture this query into user table.

    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE username = ? AND password = ? AND role = ?', (username, password_hash, role)
    ).fetchall()

    return json.dumps([dict(ix) for ix in user], indent=4, sort_keys=True, default=str)
#load the user templates from their user_id

@bp.route('/api/<int:id>/loadUser', methods=('GET', 'POST'))
def loadUser(id):
#Select the user from the query string user id.

    user = get_db().execute(
        'SELECT *'
        ' FROM user u'
        ' WHERE u.id = ?',
        (id,)
    ).fetchall()
#If the user id doesnt exist on the table return the f string.

    if user is None:
        abort(404, f"User id {id} doesn't exist.")

    return json.dumps([dict(ix) for ix in user], indent=4, sort_keys=True, default=str)