import re

from .error_handlers import APIError
from .models import URLMap


def validate_url_map_data(data):
    """
    Проверяет входные данные, при работе с API, на соответствие спецификации.

    Parameters
    ----------
    data : dict
        Входные данные из POST запроса

    Returns
    -------
    bool
        True - если данные соответсвуют спецификации

    Raises
    ------
    APIError
        При отсутствии тела запроса, код 400
    APIError
        При отсутствии поля "url", код 400
    APIError
        При превышении длины поля "custom_id", или несоответствия значения
        спецификации, код 400
    APIError
        При попытке добавить короткий ID, который уже уществует в БД, код 400
    """
    if data is None:
        raise APIError('Отсутствует тело запроса')
    elif 'url' not in data:
        raise APIError('"url" является обязательным полем!')

    if 'custom_id' in data:
        short = data['custom_id']
        if len(short) > 16 or re.match(r'^[a-zA-z0-9]*$', short) is None:
            raise APIError('Указано недопустимое имя для короткой ссылки')
        elif URLMap.check_short_id_exist(short):
            raise APIError(
                'Предложенный вариант короткой ссылки уже существует.'
            )

    return True
