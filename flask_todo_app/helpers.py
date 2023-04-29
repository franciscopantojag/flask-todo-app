from flask import redirect, session, g, request
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


def redirect_index_if_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "GET":
            user_id = session.get('user_id')
            if user_id:
                user = get_db().execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
                if user:
                    return redirect('/')
                else:
                    session.clear()
        return f(*args, **kwargs)
    return decorated_function
