from app import app, socketio
from flask import render_template, flash, redirect, url_for
from app.forms import VideoURL
<<<<<<< HEAD
from songflong.searchProgram import Search
from songflong.video import VideoData
from multiprocessing import Process
from threading import Thread
import json
from flask_socketio import emit
=======
from pytube import YouTube
from multiprocessing import Process
from songflong import *
import time

curVideoData = []*5

def processSearch(givenLink):
	global curVideoData

	start = time.time() # Timing
	curVideoData = []*5
	keywords = YouTube(givenLink).title
	bpm = getTrackTuneBatBPM(keywords)
	end = time.time() # Timing

	get_bpm = str(end - start) # Timing

	start = time.time() # Timing
	matches = findMatches(bpm)[:5]
	end = time.time() # Timing

	print(matches)
        
	get_matches = str(end - start) # Timing

	start = time.time() # Timing
	curVideoData.append(VideoData(url=givenLink, keywords=keywords, title=keywords))
	curVideoData.extend(search(matches))
	end = time.time() # Timing
>>>>>>> 1b11e60d06794253c75667fcf47b7e441712963e

	get_ytlinks = str(end - start)

	start = time.time() # Timing
	downloadVideos(curVideoData)
	end = time.time() # Timing

<<<<<<< HEAD
thread = Thread()
curVideoData = None
=======
	get_downloads = str(end - start)

	start = time.time() # Timing
	createVideoFiles(curVideoData)
	end = time.time() # Timing

	get_vidfiles = str(end - start) # Timing

	print("Get video BPM: %s\nGet video matches: %s\nGet matching videos' links: %s\nDownload audio/video streams from matching videos' links: %s\nGenerate Video Files: %s\n" % (get_bpm, get_matches, get_ytlinks, get_downloads, get_vidfiles))
>>>>>>> 1b11e60d06794253c75667fcf47b7e441712963e

@app.route('/', methods=['GET', 'POST'])
def index():
    global curVideoData, thread
    form = VideoURL()
    if form.validate_on_submit():
        if not thread.isAlive():
            print("Starting Thread")
            thread = Search(form.url.data)
            temp = thread.start()

            socketio.emit('my event',{'data': json.dumps(temp)})
        return redirect(url_for('index'))

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

@socketio.on('my event', namespace='/test')
def test_message(message):
    print(message['data']);

    thread = Search(message['data'])
    thread.start()
    temp = thread.join()
    print("Uploading")
    j = json.dumps(temp)
    if not temp is None:
        emit('my response',j)
