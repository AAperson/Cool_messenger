from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class FriendForm(FlaskForm):
    alias = StringField('Псевдоним', validators=[DataRequired()])
    submit = SubmitField('Добавить')