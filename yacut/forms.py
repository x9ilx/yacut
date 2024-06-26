from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLMapForm(FlaskForm):
    """URLMapForm описания формы для html-шаблона."""

    original_link = URLField(
        'Длинная ссылка', validators=[DataRequired('Это обязательное поле')]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(
                0, 16, 'Длина не может быть меньше 1, и больше 16 символов'
            ),
            Optional(),
        ],
    )
    submit = SubmitField('Создать')
