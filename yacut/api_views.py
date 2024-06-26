from flask import jsonify, request

from . import app, db
from .error_handlers import APIError
from .models import URLMap
from .validators import validate_url_map_data


@app.route('/api/id/', methods=['POST'])
def create_url_map():
    data = request.get_json(silent=True)

    if validate_url_map_data(data):
        short = ''

        if 'custom_id' not in data:
            short = URLMap.generate_unique_short_id()
        else:
            short = data['custom_id']

        url_map = URLMap(original=data['url'], short=short)   # type: ignore
        db.session.add(url_map)
        db.session.commit()
        return jsonify(url_map.to_dict()), 201
    raise APIError('Что-то пошло не так.')


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_full_url(short):
    url_map = URLMap.query.filter_by(short=short).first()

    if url_map is None:
        raise APIError('Указанный id не найден', 404)

    return jsonify({'url': url_map.original}), 200
