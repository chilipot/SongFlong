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
from .user import User

thread = Thread()
thread_stop_event = Event()

class Search(Thread):
    def __init__(self, user, _return=None):
        super(Search, self).__init__()
        self.user = user
        self.givenLink = user.ytURL
        self._return = _return

    def processSearch(self):
        curVideoData = self.user.data
        keywords = YouTube(self.givenLink).title
        bpm = getTrackTuneBatBPM(keywords)
        matches = findMatches(bpm)[:5]
        print(matches)
        self.user.data.append(VideoData(url=self.givenLink, keywords=keywords, title=keywords))
        self.user.data.extend(search(matches))
        print("downloading")
        print(self.user.data)
        downloadVideos(self.user)
        print("Final videos")
        print(self.user.data)
        createVideoFiles(self.user)
        print("Files made")
        print(self.user.data)
        print(self.user.data[0])

    def run(self):
        print("running")
        self.processSearch()
        print("files found")
        print(self.user)
        self.user = [json.loads(json.dumps(videodata, cls=ComplexEncoder)) for videodata in self.user.data]
        self._return = self.user

    def join(self, *args):
        Thread.join(self, *args)
        return self._return
