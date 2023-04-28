from flask import Blueprint, request, session, redirect, render_template, flash
from flask_todo_app.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        user_id = session.get('user_id')
        if user_id:
            user = get_db().execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            if user:
                return redirect('/')
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Username and Password are required', 'error')
        return render_template('login.html'), 400
    
    user = get_db().execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

    if not user:
        flash('Username not found', 'error')
        return render_template('login.html'), 404
    
    if not check_password_hash(user['password'], password):
        flash('Wrong password', 'error')
        return render_template('login.html'), 401

    session.clear()
    session["user_id"] = user["id"]

    flash('Login succeded', 'message')
    return redirect('/')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        user_id = session.get('user_id')
        if user_id:
            user = get_db().execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            if user:
                return redirect('/')
        return render_template('login.html', register=True)

    username = request.form.get('username', '').strip()
    password = request.form.get('password')
    confirmation = request.form.get('confirmation')

    if not username or not password or not confirmation:
        flash('Username, password, and confirmation are required', 'error')
        return render_template('login.html', register=True), 400

    if password != confirmation:
        flash('Password and Confirm Password must match', 'error')
        return render_template('login.html', register=True), 400
    
    db = get_db()

    duplicates = db.execute('SELECT username FROM users WHERE username = ?', (username,)).fetchall()
    if duplicates:
        flash('Username taken', 'error')
        return render_template('login.html', register=True), 400
    
    cursor = db.cursor()
    cursor.execute('INSERT INTO users(username, password) VALUES(?, ?)',
                        (username, generate_password_hash(password)))
    db.commit()
    user_id = cursor.lastrowid

    session.clear()
    session["user_id"] = user_id

    flash('User created', 'message')
    return redirect('/')