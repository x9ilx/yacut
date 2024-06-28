from flask import abort, redirect, render_template

from . import app
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
    except Exception:
        abort(500)
    return render_template('index.html', form=form, short=url_map.short_url)


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
    return redirect(
        URLMap.get_full_url_from_short(short)
    )
