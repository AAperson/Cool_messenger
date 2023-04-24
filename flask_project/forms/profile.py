from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired


class Profile(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    sex = StringField('Пол')
    foto = FileField('Аватарка')
    city = StringField('Город проживания', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
