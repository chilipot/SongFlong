from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import VideoURL
from pytube import YouTube
from tunebat import findMatches, getTrackTuneBatBPM
from youtubeSearch import findAllLinks as search
from download import run as downloadVideos
from contructVideo import createVideoFiles
from video import VideoData
from multiprocessing import Process

curVideoData = []*5


def processSearch(givenLink):
    global curVideoData
    curVideoData = []*5
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
        Process(processSearch(form.url.data)).start()
        return redirect(url_for('index'))
    print(curVideoData)
    if curVideoData:
        return render_template('theonlyhtmlfileweneed.html', title='Song Flong', form=form, videoData=curVideoData[1:])
    else:
        temp = [VideoData(None, title="Call Me Maybe", final='static/demo/video1.mp4', artist='Carly Rae Jepsen', art='https://upload.wikimedia.org/wikipedia/en/thumb/a/ad/Carly_Rae_Jepsen_-_Call_Me_Maybe.png/220px-Carly_Rae_Jepsen_-_Call_Me_Maybe.png'),
        VideoData(None, title="Harder", final='static/demo/video2.mp4', artist='Tiesto & Amp', art='https://upload.wikimedia.org/wikipedia/en/thumb/9/9a/Ti%C3%ABsto_and_KSHMR_Harder.jpg/220px-Ti%C3%ABsto_and_KSHMR_Harder.jpg'),
        VideoData(None, title="Hot N Cold", final='static/demo/video3.mp4', artist='Katy Perry', art='https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/Hot_N_Cold_%28Official_Single_Cover%29_by_Katy_Perry.png/220px-Hot_N_Cold_%28Official_Single_Cover%29_by_Katy_Perry.png'),
        VideoData(None, title="On The Floor", final='static/demo/video4.mp4', artist='Jennifer Lopez Feat. Pitbull', art='https://upload.wikimedia.org/wikipedia/en/thumb/9/91/On_the_Floor.png/220px-On_the_Floor.png'),
        VideoData(None, title="Sexy And I Know It", final='static/demo/video5.mp4', artist='LMFAO', art='https://upload.wikimedia.org/wikipedia/en/thumb/7/76/Sexy_and_I_Know_It_-_Single.png/220px-Sexy_and_I_Know_It_-_Single.png'),
        VideoData(None, title="placeholder", final='static/demo/video6.mp4', artist='placeholder', art=None)]
        return render_template('theonlyhtmlfileweneed.html', title='Song Flong', form=form, videoData=temp)
