import uuid
from datetime import datetime

from flask import request

from . import db


class URLMap(db.Model):
    """URLMap модель соответствия длинной и короткой ссылки."""

    id = db.Column(db.Integer(), primary_key=True)
    original = db.Column(db.String())
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': f'{request.host_url}{self.short}',
        }

    @staticmethod
    def generate_unique_short_id():
        """
        Генерирует уникальный короткий ID.

        Returns
        -------
        str
            Сгенерированный ID
        """
        unique_id = uuid.uuid4().hex[:6]
        while URLMap.query.filter_by(short=unique_id).first() is not None:
            unique_id = uuid.uuid4().hex[:6]

        return unique_id

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
