from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import VideoURL
from pytube import YouTube
from tunebat import findMatches, getTrackTuneBatBPM
from youtubeSearch import findAllLinks as search
from download import run as downloadVideos
from contructVideo import createVideoFiles

def processSearch(givenLink):
    flash('Converting video')
    print(givenLink.data)
    keywords = YouTube(givenLink.data).title
    bpm = getTrackTuneBatBPM(keywords)
    matches = findMatches(bpm)[0:5]
    print(matches)
    matchlinks = [givenLink.data]
    matchlinks.extend(search(matches))
    print(matchlinks)
    files = downloadVideos(matchlinks)
    createVideoFiles(files)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = VideoURL()
    print('anything')
    if form.validate_on_submit():
        flash('valid input')
        processSearch(form.url)
        return redirect(url_for('index'))
    return render_template('theonlyhtmlfileweneed.html', title='Song Fling Flong', form=form)
