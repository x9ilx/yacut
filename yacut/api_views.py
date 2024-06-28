from http import HTTPStatus

from flask import jsonify, request

from . import app, text
from .error_handlers import APIError
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_url_map():
    """
    API для создания новой записи соответствия ссылки и короткого ID.

    Returns
    -------
    Response
        Ответ на запрос в формате json

    Raises
    ------
    APIError
        В случае, если запрос неверен
    """
    data = request.get_json(silent=True)
    if data is None:
        raise APIError(text.EMPTY_QUERY)
    elif 'url' not in data:
        raise APIError(text.QUERY_WITHOUT_URL)
    short = data.get('custom_id', None)
    url_map = URLMap.create(original=data['url'], short=short)
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_full_url(short):
    """
    API для получение исходной ссылки по короткому ID.

    Parameters
    ----------
    short : str
        Короткий ID

    Returns
    -------
    Response
        Ответ на запрос в формате json

    Raises
    ------
    APIError
        В случае, если запрос неверен
    """
    return jsonify(
        {
            'url': URLMap.get_full_url_from_short(short)
        }
    ), HTTPStatus.OK
