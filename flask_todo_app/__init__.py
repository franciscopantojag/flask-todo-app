import os
from flask import Flask, session, render_template, redirect, request, flash, g
from flask_todo_app.helpers import login_required
from flask_todo_app.db import get_db
from flask_todo_app import auth, todo
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "todo.sqlite"),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from flask_todo_app import db
    db.init_app(app)

    @app.route('/')
    @login_required
    def index():
        db = get_db()
        user_id = session.get('user_id')

        user = db.execute('SELECT username FROM users WHERE id = ?', (user_id,)).fetchone()

        if not user:
            session.clear()
            return redirect('/login')

        todos = db.execute(
            'SELECT todo, deadline, id, done FROM todos WHERE user_id=?', (user_id,)).fetchall()
        return render_template('index.html', todos=todos, user=user)
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)

    return app