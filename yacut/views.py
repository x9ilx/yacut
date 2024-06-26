from flask import flash, redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def generate_link():
    form = URLMapForm()
    context = {
        'form': form,
    }
    if form.validate_on_submit():
        short = form.custom_id.data

        if short:
            if URLMap.check_short_id_exist(short):
                flash(
                    'Предложенный вариант короткой ссылки уже существует.',
                    'error',
                )
                return render_template('generate_link.html', form=form)
        else:
            short = URLMap.generate_unique_short_id()

        url_map = URLMap(
            original=form.original_link.data,
            short=short,
        )   # type: ignore

        db.session.add(url_map)
        db.session.commit()

        context.update({'url_map': url_map})
    return render_template('generate_link.html', **context)


@app.route('/<string:short>')
def redirect_view(short):
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_map.original)
