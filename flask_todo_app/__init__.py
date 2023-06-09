import os
from flask import Flask, render_template, g
from flask_todo_app.helpers import login_required
from flask_todo_app.db import get_db
from flask_todo_app import auth, todo, db


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

    db.init_app(app)

    @app.route('/')
    @login_required
    def index():
        todos = get_db().execute(
            'SELECT todo, deadline, id, done FROM todos WHERE user_id=?', (g.user['id'],)).fetchall()
        return render_template('index.html', todos=todos, user=g.user)

    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)

    return app
