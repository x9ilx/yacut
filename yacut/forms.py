from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import (DataRequired, Length, Optional, Regexp,
                                ValidationError)

from .constants import (ORIGINAL_LINK_MAX_LENGTH, SHORT_MAX_LENGTH_FOR_USER,
                        SHORT_PATTERN)
from .models import URLMap

FORM_REQUIRED_FIELD = 'Это обязательное поле'
ORIGINAL_EXCEEDING_MAX_LENGTH = (
    f'Длина не может быть больше {ORIGINAL_LINK_MAX_LENGTH} символов'
)
SHORT_EXCEEDING_MAX_LENGTH = (
    f'Длина не может быть больше {SHORT_MAX_LENGTH_FOR_USER} символов'
)
INVALID_SHORT_NAME = 'Указано недопустимое имя для короткой ссылки'
SHORT_ALREADY_EXIST = 'Предложенный вариант короткой ссылки уже существует.'
ORIGINAL_FIELD_NAME = 'Длинная ссылка'
SHORT_FIELD_NAME = 'Ваш вариант короткой ссылки'
SUBMIT_BUTTON_TEXT = 'Создать'


class URLMapForm(FlaskForm):
    """URLMapForm описания формы для html-шаблона."""

    original_link = URLField(
        ORIGINAL_FIELD_NAME,
        validators=[
            DataRequired(FORM_REQUIRED_FIELD),
            Length(
                max=ORIGINAL_LINK_MAX_LENGTH,
                message=ORIGINAL_EXCEEDING_MAX_LENGTH,
            ),
        ],
    )
    custom_id = URLField(
        SHORT_FIELD_NAME,
        validators=[
            Length(
                max=SHORT_MAX_LENGTH_FOR_USER,
                message=SHORT_EXCEEDING_MAX_LENGTH,
            ),
            Regexp(regex=SHORT_PATTERN, message=INVALID_SHORT_NAME),
            Optional(),
        ],
    )
    submit = SubmitField(SUBMIT_BUTTON_TEXT)

    def validate_custom_id(form, field):
        if URLMap.get_url_map_from_short(field.data):
            raise ValidationError(SHORT_ALREADY_EXIST)
