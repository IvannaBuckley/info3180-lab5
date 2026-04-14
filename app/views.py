from app.forms import MovieForm
from app.models import Movie
from app import db
from werkzeug.utils import secure_filename


"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from flask import Blueprint, render_template, request, jsonify, current_app
import os

main = Blueprint('main', __name__)



@main.route('/movies/create', methods=['GET', 'POST'])
def create_movie():
    form = MovieForm()

    if form.validate_on_submit():
        poster_file = form.poster.data
        filename = secure_filename(poster_file.filename)

        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        poster_file.save(os.path.join(upload_folder, filename))

        movie = Movie(
            title=form.title.data,
            description=form.description.data,
            poster=filename
        )

        db.session.add(movie)
        db.session.commit()

        return jsonify(message="Movie saved successfully!")

    return render_template('create_movie.html', form=form)


def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            )
            error_messages.append(message)

    return error_messages


@main.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return current_app.send_static_file(file_dot_text)


@main.after_app_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@main.app_errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404