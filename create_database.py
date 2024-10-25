from app import app, database
from app.models import User, Image

with app.app_context():
    database.create_all()