from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import VideoURL
from pytube import YouTube
from tunebat import findMatches, getTrackTuneBatBPM
from youtubeSearch import findAllLinks as search
from download import run as downloadVideos
from contructVideo import createVideoFiles
from video import VideoData

results = [None] * 6
matches = [""] * 5
curVideoData = []


def processSearch(givenLink):
    global curVideoData, results
    keywords = YouTube(givenLink).title
    bpm = getTrackTuneBatBPM(keywords)
    matches = findMatches(bpm)[:5]
    print(matches)
    curVideoData.append(VideoData(url=givenLink, keywords=keywords, title=keywords))
    curVideoData.extend(search(matches))
    print(curVideoData)
    downloadVideos(curVideoData)
    createVideoFiles(curVideoData)
    print(curVideoData)
    print(curVideoData[0])
    print(curVideoData[0].final)
    results = list(map(lambda data: url_for('static', filename=data.final), curVideoData[1:]))






@app.route('/', methods=['GET', 'POST'])
def index():
    form = VideoURL()
    if form.validate_on_submit():
        processSearch(form.url.data)
        return redirect(url_for('index'))
    print(results)
    print(matches)
    return render_template('theonlyhtmlfileweneed.html', title='Song Flong', form=form, titles=list(map(lambda data: data.title, curVideoData[1:])), video=results)
