from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import APIError, ModelError
from .models import URLMap

EMPTY_QUERY = 'Отсутствует тело запроса'
QUERY_WITHOUT_URL = '"url" является обязательным полем!'


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
        raise APIError(EMPTY_QUERY)
    if 'url' not in data:
        raise APIError(QUERY_WITHOUT_URL)
    try:
        return (
            jsonify(
                URLMap.create(
                    original=data['url'],
                    short=data.get('custom_id'),
                    validate_short=True,
                ).to_dict()
            ),
            HTTPStatus.CREATED,
        )
    except ModelError as error:
        raise APIError(error.message)


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
    try:
        return (
            jsonify({'url': URLMap.get_full_url_from_short(short)}),
            HTTPStatus.OK,
        )
    except ModelError as error:
        raise APIError(error.message, status_code=HTTPStatus.NOT_FOUND)
