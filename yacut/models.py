import random
import re
from datetime import datetime
from http import HTTPStatus

from flask import abort, url_for
from .constants import (ALLOWED_SYMBOLS_FOR_SHORT,
                      NUMBER_OF_SHORT_GENERATION_PASSES, SHORT_LENGTH,
                      ORIGINAL_LINK_MAX_LENGTH, SHORT_MAX_LENGTH_FOR_USER)

from . import db, text
from . error_handlers import APIError


class URLMap(db.Model):
    """URLMap модель соответствия длинной и короткой ссылки."""

    id = db.Column(db.Integer(), primary_key=True)
    original = db.Column(db.String(ORIGINAL_LINK_MAX_LENGTH))
    short = db.Column(db.String(SHORT_MAX_LENGTH_FOR_USER), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': f'{self.short_url}',
        }

    @property
    def short_url(self):
        return url_for('redirect_view', short=self.short, _external=True)

    @staticmethod
    def get_full_url_from_short(short):
        url_map = URLMap.query.filter_by(short=short).first()
        if url_map is None:
            raise APIError(text.ID_NOT_EXIST, HTTPStatus.NOT_FOUND)
        return url_map.original

    @staticmethod
    def create(original, short=None):
        """
        Создаёт запись в БД.

        Returns
        -------
        URLMap
            Экземпляр URLMap созданного объекта
        """
        if short:
            if (len(short) > SHORT_MAX_LENGTH_FOR_USER
                or re.match(r'^[a-zA-z0-9]*$', short) is None):
                raise APIError(text.INVALID_SHORT_NAME)
            elif URLMap.query.filter_by(short=short).first() is not None:
                raise APIError(text.SHORT_ALREADY_EXIST)
        else:
            for _ in range(0, NUMBER_OF_SHORT_GENERATION_PASSES):
                short = ''
                for _ in range(0, SHORT_LENGTH):
                    short += random.choice(ALLOWED_SYMBOLS_FOR_SHORT)
                if URLMap.query.filter_by(short=short).first() is None:
                    break
            else:
                raise APIError(
                    'Не удалось сгенерировать короткую ссылку.'
                )
            
        url_map = URLMap(
            original=original,
            short=short,
        )   # type: ignore
        db.session.add(url_map)
        db.session.commit()
        return url_map
