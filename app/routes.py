from app import app
from flask import render_template
from app.forms import VideoURL

@app.route('/', methods=['GET', 'POST'])
def index():
    form = VideoURL()
    if form.validate_on_submit():
        flask('Converting video')
        return redirect(url_for('index'))
    return render_template('theonlyhtmlfileweneed.html', title='dan was here', form=form)
