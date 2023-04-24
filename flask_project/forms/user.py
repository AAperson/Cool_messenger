from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, IntegerField, SubmitField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repeat_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    sex = StringField('Пол')
    foto = FileField('Аватарка')
    alias = StringField('Псевдоним', validators=[DataRequired()])
    city = StringField('Город проживания', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')