from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from flaskr.auth import login_required
from flaskr.db import get_db

import folium
import json
from flask import jsonify

bp = Blueprint('feedback', __name__)

@bp.route('/')
def index():
    return render_template('card/index.html')

@bp.route('/api/listFeedback', methods=('GET', 'POST'))
def listFeedback():
    uid = request.args.get('uid')
    db = get_db()

    feedbacks = db.execute(
        'SELECT *'
        ' FROM feedback c JOIN user u ON c.user_id = u.id'
        ' WHERE c.user_id = ?'
        #' ORDER BY created DESC'
        (uid,)
    ).fetchall()

    return json.dumps([dict(ix) for ix in feedbacks], indent=4, sort_keys=True, default=str)

@bp.route('/api/createFeedback', methods=('GET', 'POST'))
def createFeedback():
    data = request.get_json()

    if request.method == 'POST':
        uid = data.get('uid')
        description = data.get('description')
        feedback = data.get('feedback')
        error = None

        if not description:
            error = 'Description is required.'
        if not feedback:
            error = 'Feedback is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO feedback (user_id, description, feedback)'
                ' VALUES (?, ?, ?)',
                (uid, description, feedback)
            )
            db.commit()
            return json.dumps({'success':True}), 201, {'ContentType':'application/json'}

@bp.route('/api/<int:id>/getFeedback', methods=('GET', 'POST'))
def getFeedback(id):

    feedback = get_db().execute(
        'SELECT *'
        ' FROM feedback f JOIN user u ON f.user_id = u.id'
        ' WHERE f.id = ?',
        (id,)
    ).fetchall()

    if feedback is None:
        abort(404, f"Feedback id {id} doesn't exist.")

    return json.dumps([dict(ix) for ix in feedback], indent=4, sort_keys=True, default=str)

def get_feedback_local(id, check_author=True):
    data = request.get_json()
    if data.get('id'):
        id = data.get('id')

    feedback = get_db().execute(
        'SELECT *'
        ' FROM feedback f JOIN user u ON f.user_id = u.id'
        ' WHERE f.id = ?',
        (id,)
    ).fetchone()

    if feedback is None:
        abort(404, f"Feedback id {id} doesn't exist.")

    return feedback

@bp.route('/api/<int:id>/updateFeedback', methods=('GET', 'POST'))
def updateFeedback(id):
    data = request.get_json()

    if request.method == 'POST':
        uid = data.get('uid')
        description = data.get('description')
        feedback_info = data.get('feedback_info')
        error = None

        feedback = get_feedback_local(id)

        if not description:
            error = 'Description is required.'
        if not feedback:
            error = 'Feedback is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE feedback SET description = ?, feedback = ?'
                ' WHERE id = ?',
                (description, feedback_info, id)
            )
            db.commit()
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@bp.route('/api/<int:id>/deleteFeedback', methods=('POST',))
def deleteFeedback(id):
    db = get_db()
    db.execute('DELETE FROM feedback WHERE id = ?', (id,))
    db.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}