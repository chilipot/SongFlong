from pytube import YouTube
from .tunebat import findMatches, getTrackTuneBatBPM
from .youtubeSearch import findAllLinks as search
from .download import run as downloadVideos
from .constructVideo import createVideoFiles
from .video import VideoData
from multiprocessing import Process
from threading import Thread, Event
import json
from app import socketio
from .complex_json_encoder import *

thread = Thread()
thread_stop_event = Event()

class Search(Thread):
    def __init__(self, givenLink, _return=None):
        super(Search, self).__init__()
        self.givenLink = givenLink
        self._return = _return

    def processSearch(self):
        curVideoData = []*5
        keywords = YouTube(self.givenLink).title
        bpm = getTrackTuneBatBPM(keywords)
        matches = findMatches(bpm)[:5]
        print(matches)
        curVideoData.append(VideoData(url=self.givenLink, keywords=keywords, title=keywords))
        curVideoData.extend(search(matches))
        print(curVideoData)
        downloadVideos(curVideoData)
        createVideoFiles(curVideoData)
        print(curVideoData)
        print(curVideoData[0])
        print(curVideoData[0].final)
        return curVideoData

    def run(self):
        print("running")
        temp = self.processSearch()
        print("files found")
        print(temp)
        temp = [json.loads(json.dumps(videodata, cls=ComplexEncoder)) for videodata in temp]
        self._return = temp

    def join(self, *args):
        Thread.join(self, *args)
        return self._return
