from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import VideoURL
from pytube import YouTube
from tunebat import findMatches, getTrackTuneBatBPM
from youtubeSearch import findAllLinks as search
from download import run as downloadVideos
from contructVideo import createVideoFiles

results = [None] * 6

def processSearch(givenLink):
    global results
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
    results = createVideoFiles(files)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = VideoURL()
    print('anything')
    if form.validate_on_submit():
        flash('valid input')
        processSearch(form.url)
        return redirect(url_for('index'))
<<<<<<< HEAD
    return render_template('theonlyhtmlfileweneed.html', title='dan was here', form=form, video_1=results[0], video_2=results[1], video_3=results[2], video_4=results[3], video_5=results[4])
=======
    return render_template('theonlyhtmlfileweneed.html', title='Song Fling Flong', form=form)
>>>>>>> 797410659681ddf8b30af5921f40b830a580c69c
