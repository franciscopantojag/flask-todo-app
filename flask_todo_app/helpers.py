from flask import redirect, session, g
from functools import wraps
from flask_todo_app.db import get_db


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id == None:
            return redirect("/auth/login")
        user = get_db().execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        if not user:
            session.clear()
            return redirect("/auth/login")
        g.user = user
        return f(*args, **kwargs)
    return decorated_function
