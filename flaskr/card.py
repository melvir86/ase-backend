from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import folium

bp = Blueprint('card', __name__)

@bp.route('/')
def index():
    return render_template('card/index.html')

@bp.route('/listCard')
def listCard():
    db = get_db()
    cards = db.execute(
        'SELECT *'
        ' FROM card c JOIN user u ON c.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('card/list.html', cards=cards)

@bp.route('/createCard', methods=('GET', 'POST'))
@login_required
def createCard():
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        expiry_month = request.form['expiry_month']
        expiry_year = request.form['expiry_year']
        cve = request.form['cve']
        description = request.form['description']
        status = request.form['status']
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
                (g.user['id'], name, number, expiry_month, expiry_year, cve, description, status)
            )
            db.commit()
            return redirect(url_for('card.listCard'))

    return render_template('card/create.html')

def get_card(id, check_author=True):
    post = get_db().execute(
        'SELECT *'
        ' FROM card c JOIN user u ON c.user_id = u.id'
        ' WHERE c.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Card id {id} doesn't exist.")

    if check_author and post['user_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/updateCard', methods=('GET', 'POST'))
@login_required
def updateCard(id):
    card = get_card(id)

    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        expiry_month = request.form['expiry_month']
        expiry_year = request.form['expiry_year']
        cve = request.form['cve']
        description = request.form['description']
        status = request.form['status']
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
                'UPDATE card SET name = ?, number = ?, expiry_month = ?, expiry_year = ?, cve = ?, description = ?, status = ?'
                ' WHERE id = ?',
                (name, number, expiry_month, expiry_year, cve, description, status, id)
            )
            db.commit()
            return redirect(url_for('card.listCard'))

    return render_template('card/update.html', card=card)

@bp.route('/<int:id>/deleteCard', methods=('POST',))
@login_required
def deleteCard(id):
    get_card(id)
    db = get_db()
    db.execute('DELETE FROM card WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('card.listCard'))