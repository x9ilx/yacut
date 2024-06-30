from flask import abort, flash, redirect, render_template

from . import app
from .error_handlers import ModelError, ModelErrorType
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
        url_map = URLMap.create(
            original=form.original_link.data,
            short=form.custom_id.data,
        )
    except ModelError as error:
        if error.error_type == ModelErrorType.DB:
            abort(error.error_type.value)
        flash(error.message)
    return render_template(
        'index.html',
        form=form,
        short_url=url_map.short_url,
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
    except ModelError as error:
        abort(error.error_type.value)
