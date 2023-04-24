from flask_wtf import FlaskForm
from wtforms import BooleanField, FileField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    about = TextAreaField('Что у вас нового?', validators=[DataRequired()])
    is_private = BooleanField('Показывать только друзьям')
    img = FileField('Прикрепить фото')
    submit = SubmitField('Подтвердить')
