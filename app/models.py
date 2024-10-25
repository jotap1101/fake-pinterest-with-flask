from app import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(255), unique=True, nullable=False)
    email = database.Column(database.String(255), unique=True, nullable=False)
    password = database.Column(database.String(255), nullable=False)
    images = database.relationship('Image', backref='user', lazy=True)
    created_at = database.Column(database.DateTime, default=datetime.utcnow(), nullable=False)

class Image(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    image = database.Column(database.String(255), default='default.png', nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    created_at = database.Column(database.DateTime, default=datetime.utcnow(), nullable=False)