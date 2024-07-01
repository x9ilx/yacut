from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app
from .error_handlers import ModelError
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """
    Эндпоинт главной страницы с формой, для создания новой записи в БД.
    Returns
    -------
    str
        HTML-код шаблона "index.html"
    """
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_link=URLMap.create(
                original=form.original.data,
                short=form.short.data,
            ).short_link,
        )
    except ModelError as error:
        flash(str(error))
    return render_template(
        'index.html',
        form=form,
    )


@app.route('/<string:short>')
def redirect_view(short):
    """
    Эндпоинт для перенапралвения пользователя по исходной ссылки,
    при сопоставлении с коротким ID.

    Parameters
    ----------
    short : str
        Короткий ID

    Returns
    -------
    Response
        Ответ на запрос с перенаправлением
    """
    try:
        return redirect(URLMap.get_full_url_from_short(short))
    except ModelError:
        abort(HTTPStatus.NOT_FOUND)
