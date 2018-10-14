import requests
import json
import urllib
from bs4 import BeautifulSoup, NavigableString
import complex_json_encoder as cje
from video import VideoData

def getTrackTuneBatBPM(query):
    encodedQueryString = urllib.parse.urlencode({'q' : query})
    url = "https://tunebat.com/Search?" + encodedQueryString
    r = requests.get(url).content
    soup = BeautifulSoup(r, 'lxml')

    resultElem = soup.find(class_="search-info-container")

    bpm = int(resultElem.find_all(class_="row search-attribute-value")[2].string)

    return bpm

class Song(cje.ComplexJSONSerializable):
    def __init__(self, title, artist, bpm, relPopularity):
        self.title = title
        self.artist = artist
        self.bpm = bpm
        self.relPopularity = relPopularity


def getSongsByBPM(targetBPM, pageNum=1):
    url = "https://jog.fm/popular-workout-songs?bpm=" + str(targetBPM) + "&page=" + str(pageNum)

    page = requests.get(url).content

    soup = BeautifulSoup(page, 'lxml')

    entries =  soup.find_all(class_="song list-item")

    songs = []

    for i, entry in enumerate(entries):
        titleParent = entry.findChild("div", class_="title")
        artistParent = entry.findChild("div", class_="top")
        bpmParent = entry.findChild("div", class_="side-box fixed")
        bpmParent = bpmParent.findChild("div", class_="middle") if bpmParent is not None else bpmParent

        if (titleParent is not None and artistParent is not None and bpmParent is not None):
            title = titleParent.a.string
            artist = artistParent.a.string
            bpm = bpmParent.a.string

            songs += [Song(title, artist, int(bpm), int(i))]

        #print(title)

    songs.sort(key=lambda song : (abs(targetBPM - song.bpm), song.relPopularity))

    return json.loads(json.dumps(songs, cls=cje.ComplexEncoder))

def findMatches(bpm):
    matches = getSongsByBPM(bpm)

    return list(map(lambda match: VideoData(keywords=(match['title'] + " " + match['artist']),title=match['title']), matches))



if __name__ == '__main__':
    #print(findMatches(126))
    bpm = getTrackTuneBatBPM("All Day and all of the night")
