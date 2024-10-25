from app.models import *
from flask_wtf import FlaskForm
from wtforms import FileField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

class LoginForm(FlaskForm):
    email = StringField(
        label='Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        label='Senha',
        validators=[
            DataRequired()
        ]
    )
    button = SubmitField(label='Entrar')

class RegisterForm(FlaskForm):
    username = StringField(
        label='Nome de Usuário',
        validators=[
            DataRequired()
        ]
    )
    email = StringField(
        label='Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        label='Senha',
        validators=[
            DataRequired(),
            Length(6, 20)
        ]
    )
    confirm_password = PasswordField(
        label='Confirmar Senha',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    button = SubmitField(label='Criar Conta')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Username already taken.') 
        
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already taken.')
    
    def validate_password(self, password):
        if len(password.data) < 6:
            raise ValidationError('Password must be at least 6 characters long.')
        elif len(password.data) > 20:
            raise ValidationError('Password must be at most 20 characters long.')
    
    def validate_confirm_password(self, confirm_password):
        if self.password.data != confirm_password.data:
            raise ValidationError('Passwords do not match.')
    
class ImageForm(FlaskForm):
    image = FileField(
        label='Image',
        validators=[
            DataRequired()
        ]
    )
    button = SubmitField(label='Submit')

    def validate_image(self, image):
        if not image.data.filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            raise ValidationError('Invalid image format.')
    