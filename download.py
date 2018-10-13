from pytube import YouTube
import os
import time
import sys


link = 'https://www.youtube.com/watch?v=oHg5SJYRHA0'

class Video:
    def __init__(self, url):
        self.url = url
        self.yt = YouTube(url)
        self.title = self.yt.title

    def getStreamsVA(self):
        self.yt.prefetch()
        self.yt.register_on_complete_callback(self.filesDownloaded)
        audio = self.yt.streams.filter(only_audio=True, subtype='mp4', adaptive=True).order_by('abr').desc().first()
        video = self.yt.streams.filter(only_video=True, subtype='mp4', adaptive=True).order_by('resolution').desc().first()

        return audio, video

    def downloadStreams(self, audio, video):
        downloadPath = os.getcwd() + r'\tmp'
        audio.download(output_path=downloadPath,filename='originala')
        video.download(output_path=downloadPath,filename='originalv')

    def filesDownloaded(self, stream, file_handle):
        print(file_handle.name)



video = Video(link)
a, v = video.getStreamsVA()
video.downloadStreams(a, v)
