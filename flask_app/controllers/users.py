from flask import redirect, session, request, flash
from flask_app import app
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/register', methods=['POST'])
def register():
    if not user.User.validate(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password_register'])

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email_register'],
        'password': pw_hash
    }

    current_user = user.User.add_user(data)
    session['current_id'] = current_user
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    data = {'email': request.form['email_login']}
    email_exists = user.User.get_user_by_email(data)

    if not email_exists:
        flash('Account does not exist', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(email_exists.password, request.form['password_login']):
        flash('Invalid email/password', 'login')
        return redirect('/')

    session['current_id'] = email_exists.id
    session['owned_paintings'] = []
    return redirect('/dashboard')