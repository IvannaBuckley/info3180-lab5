# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length


class MovieForm(FlaskForm):
    title = StringField(
        'Movie Title',
        validators=[
            DataRequired(),
            Length(max=255)
        ]
    )

    description = TextAreaField(
        'Description',
        validators=[
            DataRequired()
        ]
    )

    poster = FileField(
        'Movie Poster',
        validators=[
            FileRequired(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
        ]
    )

    submit = SubmitField('Add Movie')