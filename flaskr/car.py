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

@bp.route('/api/createCar', methods=('GET', 'POST'))
def createCar():
    data = request.get_json()

    if request.method == 'POST':
        uid = data.get('uid')
        brand = data.get('brand')
        model = data.get('model')
        colour = data.get('colour')
        next_service =  data.get('next_service')
        status = data.get('status')
        error = None

        if not brand:
            error = 'Brand is required.'
        if not model:
            error = 'Model is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO car (user_id, brand, model, colour, next_service, status, pos_x, pos_y, rating)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (uid, brand, model, colour, next_service, status, 0, 0, 0)
            )
            db.commit()
            return json.dumps({'success':True}), 201, {'ContentType':'application/json'}

@bp.route('/api/<int:id>/getCar', methods=('GET', 'POST'))
def getCar(id):

    car = get_db().execute(
        'SELECT *'
        ' FROM car c JOIN user u ON c.user_id = u.id'
        ' WHERE c.id = ?',
        (id,)
    ).fetchall()

    if car is None:
        abort(404, f"Car id {id} doesn't exist.")

    return json.dumps([dict(ix) for ix in car], indent=4, sort_keys=True, default=str)

def get_car_local(id, check_author=True):
    data = request.get_json()
    if data.get('id'):
        id = data.get('id')

    car = get_db().execute(
        'SELECT *'
        ' FROM car c JOIN user u ON c.user_id = u.id'
        ' WHERE c.id = ?',
        (id,)
    ).fetchone()

    if car is None:
        abort(404, f"Car id {id} doesn't exist.")

    return car

@bp.route('/api/<int:id>/updateCar', methods=('GET', 'POST'))
def updateCar(id):
    data = request.get_json()

    if request.method == 'POST':
        uid = data.get('uid')
        brand = data.get('brand')
        model = data.get('model')
        colour = data.get('colour')
        next_service =  data.get('next_service')
        status = data.get('status')
        error = None

        car = get_car_local(id)

        if not brand:
            error = 'Brand is required.'
        if not model:
            error = 'Model is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE car SET brand = ?, model = ?, colour = ?, next_service = ?, status = ?'
                ' WHERE id = ?',
                (brand, model, colour, next_service, status, id)
            )
            db.commit()
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@bp.route('/api/<int:id>/deleteCar', methods=('POST',))
def deleteCar(id):
    db = get_db()
    db.execute('DELETE FROM car WHERE id = ?', (id,))
    db.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}