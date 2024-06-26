from flask import jsonify, render_template

from . import app


class APIError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, *args):
        super().__init__(*args)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(APIError)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
