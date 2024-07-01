import random
import re
from datetime import datetime

from flask import url_for

from . import db
from .constants import (ALLOWED_SYMBOLS_FOR_SHORT,
                        NUMBER_OF_SHORT_GENERATION_PASSES,
                        ORIGINAL_LINK_MAX_LENGTH, REDIRECT_VIEW_NAME,
                        SHORT_LENGTH, SHORT_MAX_LENGTH_FOR_USER, SHORT_PATTERN)
from .error_handlers import ModelError

ID_NOT_EXIST = 'Указанный id не найден'
INVALID_SHORT_NAME = 'Указано недопустимое имя для короткой ссылки'
SHORT_ALREADY_EXIST = 'Предложенный вариант короткой ссылки уже существует.'
GENERATE_SHORT_ERROR = (
    f'Не удалось сгенерировать короткую ссылку за '
    f'{NUMBER_OF_SHORT_GENERATION_PASSES} попыток'
)
INVALID_ORIGINAL_LENGTH = (
    f'URL должен быть указан и его длина не может '
    f'превышать {ORIGINAL_LINK_MAX_LENGTH} символов'
)


class URLMap(db.Model):
    """URLMap модель соответствия длинной и короткой ссылки."""

    id = db.Column(db.Integer(), primary_key=True)
    original = db.Column(db.String(ORIGINAL_LINK_MAX_LENGTH))
    short = db.Column(db.String(SHORT_MAX_LENGTH_FOR_USER), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': self.short_link,
        }

    @property
    def short_link(self):
        return url_for(REDIRECT_VIEW_NAME, short=self.short, _external=True)

    @staticmethod
    def get_full_url_from_short(short):
        url_map = URLMap.get(short=short)
        if url_map is None:
            raise ModelError(ID_NOT_EXIST)
        return url_map.original

    @staticmethod
    def create(original, short=None, validate_data=False):
        """
        Создаёт запись в БД.

        Returns
        -------
        URLMap
            Экземпляр URLMap созданного объекта
        """
        if short:
            if validate_data:
                if (
                    len(short) > SHORT_MAX_LENGTH_FOR_USER
                    or re.match(SHORT_PATTERN, short) is None
                ):
                    raise ModelError(INVALID_SHORT_NAME)
                elif URLMap.get(short):
                    raise ModelError(SHORT_ALREADY_EXIST)
        else:
            short = URLMap.generate_short()
        if validate_data and len(original) > ORIGINAL_LINK_MAX_LENGTH:
            raise ModelError(INVALID_ORIGINAL_LENGTH)
        url_map = URLMap(
            original=original,
            short=short,
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get(short):
        """
        Получает объект URLMap по короткому ID.

        Parameters
        ----------
        short : str
            Короткий ID
        Returns
        -------
        URLMap
            Объект URLMap
        """
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def generate_short():
        """
        Генерирует уникальный короткий ID.
        Returns
        -------
        str
            Уникальный короткий ID
        """
        for _ in range(NUMBER_OF_SHORT_GENERATION_PASSES):
            short = ''.join(
                random.sample(ALLOWED_SYMBOLS_FOR_SHORT, SHORT_LENGTH)
            )
            if not URLMap.get(short):
                return short
        raise ModelError(GENERATE_SHORT_ERROR)
