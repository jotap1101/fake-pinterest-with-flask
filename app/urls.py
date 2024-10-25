from app import app, database, bcrypt
from app.forms import *
from app.models import *
from flask import redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.utils import secure_filename
import os

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        user = User(
            username=register_form.username.data,
            email=register_form.email.data,
            password=bcrypt.generate_password_hash(register_form.password.data)
        )

        database.session.add(user)
        database.session.commit()

        return redirect(url_for('profile', user_id=user.id))

    context = {
        'register_form': register_form
    }

    return render_template('register.html', **context)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user)

            return redirect(url_for('profile', user_id=user.id))

    context = {
        'login_form': login_form
    }

    return render_template('login.html', **context)

@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/feed')
@login_required
def feed():
    images = Image.query.order_by(Image.created_at.desc()).all()

    context = {
        'images': images
    }

    return render_template('feed.html', **context)

@app.route('/profile/<user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    if int(user_id) == int(current_user.id):
        user = current_user
        image_form = ImageForm()

        if image_form.validate_on_submit():
            image_form.image.data.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(image_form.image.data.filename)))

            image = Image(
                user_id=user.id,
                image=secure_filename(image_form.image.data.filename)
            )

            database.session.add(image)
            database.session.commit()

            return redirect(url_for('profile', user_id=user.id))
    else:
        user = User.query.get(int(user_id))
        image_form = None

    context = {
        'user': user,
        'image_form': image_form
    }

    return render_template('profile.html', **context)