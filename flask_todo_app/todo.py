from flask import Blueprint, request, session, redirect, render_template, flash, g
from flask_todo_app.db import get_db
from flask_todo_app.helpers import login_required
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime

bp = Blueprint("todo", __name__, url_prefix="/todo")

@bp.route('/', methods=['POST'])
@login_required
def create():
    todo = (request.form.get('todo', '')).strip()
    deadline = request.form.get('deadline')

    if not todo:
        flash('todo is required', 'error')
        return redirect('/')
    
    if deadline:
        regex = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}')
        if not regex.fullmatch(deadline):
            flash('Invalid Date')
            return redirect('/')
        deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
    
    db = get_db()
    db.execute('INSERT INTO todos(todo, user_id, deadline) VALUES(?, ?, ?)', (todo, g.user['id'], deadline))
    db.commit()

    return redirect('/')

@bp.route('/<id>', methods=['POST', 'PUT'])
@login_required
def modify_or_delete(id):
    db = get_db()
    if request.args.get('_method') == 'DELETE':
        db.execute('DELETE FROM todos WHERE id = ? AND user_id = ?', (id, g.user['id']))
        db.commit()
        return redirect('/')
    if request.method == 'PUT':
        try:
            done = bool(dict(request.json)['done'])
        except:
            return 'Bad request', 400

        todo = db.execute(
            'SELECT * FROM toDos WHERE id = ? AND user_id = ?', (id, g.user['id'])).fetchone()
        if not todo:
            return 'Not found', 404
        
        db.execute('UPDATE toDos SET done = ? WHERE id = ? AND user_id = ?',
               (done, id, g.user['id']))
        db.commit()
        return '', 204
    return 'Bad request'