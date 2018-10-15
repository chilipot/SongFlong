from pytube import YouTube
import os
import time
import sys
import multiprocessing as mp
from math import ceil
import requests
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from urllib.error import URLError
from video import VideoData

import time # Debug

link = 'https://www.youtube.com/watch?v=fWNaR-rxAic'
link2 = 'https://www.youtube.com/watch?v=VYOjWnS4cMY'
links = ['https://www.youtube.com/watch?v=fWNaR-rxAic',
'https://www.youtube.com/watch?v=VYOjWnS4cMY']

files = {
    'video': None,
    'audio': []
}

class Video:
    def __init__(self, url):
        self.url = url
        self.yt = YouTube(url, on_complete_callback=self.filesDownloaded, on_progress_callback=self.progressBar)
        self.title = self.yt.title


    def getAudioStream(self):
        return self.yt.streams.filter(only_audio=True, subtype='mp4', adaptive=True, custom_filter_functions=[self.bitrate]).order_by('abr').desc().first()

    def getVideoStream(self):
        return self.yt.streams.filter(only_video=True, subtype='mp4', adaptive=True, custom_filter_functions=[self.resolutions]).order_by('resolution').desc().first()

    def resolutions(self, stream):
        s = stream.resolution
        return (s == '720p' or s == '1080p' or s == '480p' or s == '360p' or s == '240p' or s == '144p')

    def bitrate(self, stream):
        b = stream.abr
        return (b == "128kbps" or b == '80kbps' or b == '40kbps')

    def filesDownloaded(self, stream, file_handle):
        print(stream)
        # print(file_handle.name)
        if (stream.mime_type == 'video/mp4'):
            files['video'] = file_handle.name
        else:
            files['audio'].append(file_handle.name)
        # files.append(file_handle)

    def progressBar(self, stream, chunk,file_handle, bytes_remaining):
        size = stream.filesize
        p = (float(bytes_remaining) / float(size)) * float(100)
        if (int(p) % 5 == 0):
            print('%.2f %s' % (p, self.title))
            #print(self.yt)

def downloadStreams(data):
    downloadPath = os.getcwd() + r'\tmp'
    path = data.stream.download(output_path=downloadPath, filename=data.stream.type + data.stream.default_filename)
    data.tempLoc = path

def run(data):
    streams = []
    try:
        data[0].stream = Video(data[0].url).getVideoStream()
        streams.append(data[0])
        start = time.time() # Debug
        pool = ThreadPool(5)
        def addAudioStreams(data):
            yt = Video(data.url)
            av = yt.getAudioStream()
            if av is not None:
                data.stream = av
                streams.append(data)

        pool.map(addAudioStreams, data[1:])
        pool.close()
        pool.join()
        end = time.time() # Debug
        print("Time: " + str(end - start))

    except URLError as e:
        print("Connection Error: Check Internet Connection or YouTube Link")
    print(streams)
    pool = ThreadPool(6)
    results = pool.map(downloadStreams, streams)
    pool.close()
    pool.join()
    return(files)

if __name__ == '__main__':
    run([VideoData(keywords="test", title="test1", url='https://www.youtube.com/watch?v=_ovdm2yX4MA'), VideoData(keywords="test", title="test2", url='https://www.youtube.com/watch?v=_ovdm2yX4MA')]) #118
    print(files)
