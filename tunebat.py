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
    def __init__(self, title, artist, bpm, relPopularity, albumArt):
        self.title = title
        self.artist = artist
        self.bpm = bpm
        self.relPopularity = relPopularity
        self.albumArt = albumArt


def getSongsByBPM(targetBPM, pageNum=1):
    url = "https://jog.fm/popular-workout-songs?bpm=" + str(targetBPM) + "&page=" + str(pageNum)
    print(url)
    page = requests.get(url).content

    soup = BeautifulSoup(page, 'lxml')

    entries =  soup.find_all(class_="song list-item")

    songs = []

    for i, entry in enumerate(entries):
        titleParent = entry.findChild("div", class_="title")
        artistParent = entry.findChild("div", class_="top")
        bpmParent = entry.findChild("div", class_="side-box fixed")
        bpmParent = bpmParent.findChild("div", class_="middle") if bpmParent is not None else bpmParent
        artParent = entry.findChild('div', class_='media')

        if (titleParent is not None and artistParent is not None and bpmParent is not None):
            title = titleParent.a.string
            artist = artistParent.a.string
            bpm = bpmParent.a.string
            art = artParent.a.img['src']

            songs += [Song(title, artist, int(bpm), int(i), art)]

        #print(title)

    songs.sort(key=lambda song : (abs(targetBPM - song.bpm), song.relPopularity))

    return json.loads(json.dumps(songs, cls=cje.ComplexEncoder))

def findMatches(bpm):
    matches = getSongsByBPM(bpm)
    print("IMPORTANT: " + matches[0]['albumArt'])
    return list(map(lambda match: VideoData(keywords=(match['title'] + " " + match['artist']),title=match['title'], artist=match['artist'], art=match['albumArt']), matches))



if __name__ == '__main__':
    #print(findMatches(126))
    bpm = getTrackTuneBatBPM("All Day and all of the night")
    print(findMatches(bpm))
