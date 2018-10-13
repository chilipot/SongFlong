from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, URL

class VideoURL(FlaskForm):
    url = StringField('Video URL', validators=[InputRequired(), URL(message="Not a valid URL")])
    submit = SubmitField('Convert')
