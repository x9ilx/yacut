from http import HTTPStatus

from flask import jsonify, render_template

from . import app, db


class ModelError(Exception):
    """
    ModelError Класс исключения для неверного взаимодействия с моделями.
    """

    def __init__(self, message, *args):
        super().__init__(*args)
        self.message = message


class APIError(Exception):
    """
    APIError Класс исключения для неверного взаимодействия с API.
    """

    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None, *args):
        super().__init__(*args)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(APIError)
def invalid_api_usage(error):
    """
    При исключении APIError возвращает ответ в формате json.

    Parameters
    ----------
    error : Exeption
        Объект ошибки

    Returns
    -------
    Response
        Ответ об ошибке, в формате json
    """
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    """
    В случае возникновение ошибки, с HTML-кодом 404,
    отображает шаблон 404.html.

    Returns
    -------
    str
        HTML-код шаблона 404.html
    """
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """
    В случае возникновение ошибки, с HTML-кодом 500,
    отображает шаблон 500.html.

    Returns
    -------
    str
        HTML-код шаблона 500.html
    """
    if db.session.is_active:
        db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
