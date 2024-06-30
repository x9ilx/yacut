import random
import re
from datetime import datetime

from flask import url_for

from . import db
from .constants import (ALLOWED_SYMBOLS_FOR_SHORT,
                        NUMBER_OF_SHORT_GENERATION_PASSES,
                        ORIGINAL_LINK_MAX_LENGTH, REDIRECT_VIEW_NAME,
                        SHORT_LENGTH, SHORT_MAX_LENGTH_FOR_USER, SHORT_PATTERN)
from .error_handlers import ModelError, ModelErrorType

ID_NOT_EXIST = 'Указанный id не найден'
INVALID_SHORT_NAME = 'Указано недопустимое имя для короткой ссылки'
SHORT_ALREADY_EXIST = 'Предложенный вариант короткой ссылки уже существует.'
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
            'short_link': self.short_url,
        }

    @property
    def short_url(self):
        return url_for(REDIRECT_VIEW_NAME, short=self.short, _external=True)

    @staticmethod
    def get_full_url_from_short(short):
        url_map = URLMap.query.filter_by(short=short).first()
        if url_map is None:
            raise ModelError(ID_NOT_EXIST, ModelErrorType.NOT_FOUND)
        return url_map.original

    @staticmethod
    def create(original, short=None, from_api=False):
        """
        Создаёт запись в БД.

        Returns
        -------
        URLMap
            Экземпляр URLMap созданного объекта
        """
        if short:
            if from_api:
                if (
                    len(short) > SHORT_MAX_LENGTH_FOR_USER
                    or re.match(SHORT_PATTERN, short) is None
                ):
                    raise ModelError(INVALID_SHORT_NAME)
                elif URLMap.check_short_id_exist(short):
                    raise ModelError(SHORT_ALREADY_EXIST)
        else:
            short = URLMap.generate_short_id()
        if from_api and 1 < len(original) > ORIGINAL_LINK_MAX_LENGTH:
            raise ModelError(INVALID_ORIGINAL_LENGTH)
        url_map = URLMap(
            original=original,
            short=short,
        )   # type: ignore
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def check_short_id_exist(short):
        """
        Проверяет, существует ли объект с таким коротким ID.
        Parameters
        ----------
        short : str
            Короткий ID
        Returns
        -------
        bool
            True - объект существует
        """
        return URLMap.query.filter_by(short=short).first() is not None

    @staticmethod
    def generate_short_id():
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
            if not URLMap.check_short_id_exist(short):
                return short

        raise ModelError(
            'Не удалось сгенерировать короткую ссылку.', ModelErrorType.DB
        )
