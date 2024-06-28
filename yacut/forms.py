from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import (DataRequired, Length, Optional, Regexp,
                                ValidationError)

from . import text
from .constants import ORIGINAL_LINK_MAX_LENGTH, SHORT_MAX_LENGTH_FOR_USER
from .models import URLMap


class URLMapForm(FlaskForm):
    """URLMapForm описания формы для html-шаблона."""

    original_link = URLField(
        text.ORIGINAL_FIELD_NAME,
        validators=[
            DataRequired(text.FORM_REQUIRED_FIELD),
            Length(
                max=ORIGINAL_LINK_MAX_LENGTH,
                message=text.EXCEEDING_MAX_LENGTH.format(
                    length=ORIGINAL_LINK_MAX_LENGTH
                )
            ),
        ]
    )
    custom_id = URLField(
        text.SHORT_FIELD_NAME,
        validators=[
            Length(
                max=SHORT_MAX_LENGTH_FOR_USER,
                message=text.EXCEEDING_MAX_LENGTH.format(
                    length=SHORT_MAX_LENGTH_FOR_USER
                )
            ),
            Regexp(
                regex=r'^[a-zA-z0-9]*$',
                message=text.INVALID_SHORT_NAME
            ),
            Optional(),
        ],
    )
    submit = SubmitField(text.SUBMIT_BUTTON_TEXT)

    def validate_custom_id(form, field):
        if URLMap.query.filter_by(short=field.data).first() is not None:
            raise ValidationError(text.SHORT_ALREADY_EXIST)