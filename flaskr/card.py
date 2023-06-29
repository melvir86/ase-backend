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
bp = Blueprint('card', __name__)

@bp.route('/')
def index():
    return render_template('card/index.html')

@bp.route('/api/listCard', methods=('GET', 'POST'))
def listCard():
    db = get_db()

    cards = db.execute(
        'SELECT *'
        ' FROM car c JOIN user u ON c.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return json.dumps([dict(ix) for ix in cards], indent=4, sort_keys=True, default=str)

@bp.route('/api/createCard', methods=('GET', 'POST'))
def createCard():
    data = request.get_json()

    if request.method == 'POST':
        uid = data.get('uid')
        name = data.get('name')
        number = data.get('number')
        expiry_month = data.get('expiry_month')
        expiry_year =  data.get('expiry_year')
        cve = data.get('cve')
        description = data.get('description')
        status = data.get('status')
        error = None

        if not name:
            error = 'Name is required.'
        if not number:
            error = 'Number is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO card (user_id, name, number, expiry_month, expiry_year, cve, description, status)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (uid, name, number, expiry_month, expiry_year, cve, description, status)
            )
            db.commit()
            return json.dumps({'success':True}), 201, {'ContentType':'application/json'}

@bp.route('/api/<int:id>/getCard', methods=('GET', 'POST'))
def getCard(id):

    card = get_db().execute(
        'SELECT *'
        ' FROM card c JOIN user u ON c.user_id = u.id'
        ' WHERE c.id = ?',
        (id,)
    ).fetchall()

    if card is None:
        abort(404, f"Card id {id} doesn't exist.")

    return json.dumps([dict(ix) for ix in card], indent=4, sort_keys=True, default=str)

def get_card_local(id, check_author=True):
    data = request.get_json()
    if data.get('id'):
        id = data.get('id')

    card = get_db().execute(
        'SELECT *'
        ' FROM card c JOIN user u ON c.user_id = u.id'
        ' WHERE c.id = ?',
        (id,)
    ).fetchone()

    if card is None:
        abort(404, f"Card id {id} doesn't exist.")

    return card

@bp.route('/api/<int:id>/updateCard', methods=('GET', 'POST'))
def updateCard(id):
    data = request.get_json()

    if request.method == 'POST':
        uid = data.get('uid')
        name = data.get('name')
        number = data.get('number')
        expiry_month = data.get('expiry_month')
        expiry_year =  data.get('expiry_year')
        cve = data.get('cve')
        description = data.get('description')
        status = data.get('status')
        error = None

        card = get_card_local(id)

        if not name:
            error = 'Name is required.'
        if not number:
            error = 'Number is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE card SET name = ?, number = ?, expiry_month = ?, expiry_year = ?, cve = ?, description = ?, status = ?'
                ' WHERE id = ?',
                (name, number, expiry_month, expiry_year, cve, description, status, id)
            )
            db.commit()
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@bp.route('/api/<int:id>/deleteCard', methods=('POST',))
def deleteCard(id):
    db = get_db()
    db.execute('DELETE FROM card WHERE id = ?', (id,))
    db.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}