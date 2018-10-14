from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import VideoURL
from pytube import YouTube
from tunebat import findMatches, getTrackTuneBatBPM
from youtubeSearch import findAllLinks as search
from download import run as downloadVideos
from contructVideo import createVideoFiles
from video import VideoData

curVideoData = []*5


def processSearch(givenLink):
    global curVideoData
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






@app.route('/', methods=['GET', 'POST'])
def index():
    form = VideoURL()
    if form.validate_on_submit():
        processSearch(form.url.data)
        return redirect(url_for('index'))
    print(curVideoData)
    if curVideoData:
        return render_template('theonlyhtmlfileweneed.html', title='Song Flong', form=form, videoData=curVideoData[1:])
    else:
        temp = [VideoData(None, title="placeholder", final='static/demo/video1.mp4')]*6
        return render_template('theonlyhtmlfileweneed.html', title='Song Flong', form=form, videoData=temp)
