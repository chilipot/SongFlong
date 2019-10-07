import requests
import urllib
import re
from bs4 import BeautifulSoup


def get_track_bpm(in_query):
    query_tokens = re.split(r'[\(\[]', in_query)
    query = query_tokens[min(0, len(query_tokens))].strip()

    encoded_query_string = urllib.parse.urlencode({'q': query})
    url = "https://tunebat.com/Search?" + encoded_query_string
    r = requests.get(url).content
    soup = BeautifulSoup(r, 'lxml')
    result_elem = soup.find(class_="search-info-container")

    bpm_string = result_elem.find_all(
        class_="row search-attribute-value")[2].string
    return int(bpm_string)


def get_songs_by_bpm(target_bpm, page_num=1):
    url = "https://jog.fm/popular-workout-songs?bpm=" + \
          str(target_bpm) + "&page=" + str(page_num)
    page = requests.get(url).content

    soup = BeautifulSoup(page, 'lxml')

    entries = soup.find_all(class_="song list-item")

    songs = []

    for i, entry in enumerate(entries):
        title_parent = entry.findChild("div", class_="title")
        artist_parent = entry.findChild("div", class_="top")
        bpm_parent = entry.findChild("div", class_="side-box fixed")
        bpm_parent = bpm_parent.findChild(
            "div", class_="middle") if bpm_parent is not None else bpm_parent
        art_parent = entry.findChild('div', class_='media')

        if title_parent is not None and artist_parent is not None and bpm_parent is not None:
            title = title_parent.a.text
            artist = artist_parent.text
            bpm = bpm_parent.a.text
            art = art_parent.a.img['src']
            # print(f"Art {art}")

            songs += [dict(title=title, artist=artist, bpm=int(bpm), rel_popularity=int(i), art=art)]

    return sorted(songs, key=lambda song: (abs(target_bpm - song['bpm']), song['rel_popularity']))[:5]
