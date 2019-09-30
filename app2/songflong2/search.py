import requests
import json
import urllib
import re
from bs4 import BeautifulSoup, NavigableString

import json


class ComplexJSONSerializable:
    def reprJSON(self):
        return self.__dict__


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)


def get_track_bpm(inQuery):
    queryTokens = re.split(r'[\(\[]', inQuery)
    # print(queryTokens)
    query = queryTokens[min(0, len(queryTokens))].strip()

    encodedQueryString = urllib.parse.urlencode({'q': query})
    url = "https://tunebat.com/Search?" + encodedQueryString
    r = requests.get(url).content
    soup = BeautifulSoup(r, 'lxml')
    resultElem = soup.find(class_="search-info-container")

    bpmString = resultElem.find_all(
        class_="row search-attribute-value")[2].string

    bpm = int(bpmString)

    return bpm


class Song(ComplexJSONSerializable):
    def __init__(self, title, artist, bpm, relPopularity, albumArt):
        self.title = title
        self.artist = artist
        self.bpm = bpm
        self.relPopularity = relPopularity
        self.albumArt = albumArt


def get_songs_by_bpm(targetBPM, pageNum=1):
    url = "https://jog.fm/popular-workout-songs?bpm=" + \
        str(targetBPM) + "&page=" + str(pageNum)
    page = requests.get(url).content

    soup = BeautifulSoup(page, 'lxml')

    entries = soup.find_all(class_="song list-item")

    songs = []

    for i, entry in enumerate(entries):
        titleParent = entry.findChild("div", class_="title")
        artistParent = entry.findChild("div", class_="top")
        bpmParent = entry.findChild("div", class_="side-box fixed")
        bpmParent = bpmParent.findChild(
            "div", class_="middle") if bpmParent is not None else bpmParent
        artParent = entry.findChild('div', class_='media')

        if (titleParent is not None and artistParent is not None and bpmParent is not None):
            title = titleParent.a.string
            artist = artistParent.a.string
            bpm = bpmParent.a.string
            art = artParent.a.img['src']
            # print(f"Art {art}")

            songs += [Song(title, artist, int(bpm), int(i), art)]

    songs.sort(key=lambda song: (
        abs(targetBPM - song.bpm), song.relPopularity))

    song_data = json.loads(json.dumps(songs, cls=ComplexEncoder))[:5]

    return [f"{song['title']} {song['artist']}" for song in song_data]


if __name__ == '__main__':
    bpm = get_track_bpm("All Day and all of the night")
    print(bpm)
    songs = get_songs_by_bpm(bpm)
    print(songs)
