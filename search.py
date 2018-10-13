import requests
import json
import urllib

def getSeedId(query):
    encodedQueryString = urllib.parse.urlencode({'query' : query, 'queryType': 'track'})
    url = "https://tunebat.com/Advanced/SeedQuery?" + encodedQueryString
    r = requests.get(url).json()['TrackItems'][0]['Id']
    return r

def getOrderedBPMMatches(seedID, bpm):
    minBPMStr = str(bpm - 5)
    maxBPMStr = str(bpm + 5)
    url = "https://tunebat.com/Advanced/AdvancedQuery?inputs={%22Target%22:{%22DurationMs%22:null,%22Energy%22:null,%22Danceability%22:null,%22Valence%22:null,%22Loudness%22:null,%22Acousticness%22:null,%22Instrumentalness%22:null,%22Liveness%22:null,%22Speechiness%22:null},%22Min%22:{%22Tempo%22:" + minBPMStr + ",%22Popularity%22:30},%22Max%22:{%22Tempo%22:" + maxBPMStr + ",%22Popularity%22:100},%22TrackSeeds%22:[%22" + seedID + "%22],%22ArtistSeeds%22:[]}"
    r = requests.get(url).json()['TrackItems']
    r.sort(key=lambda item : (abs(bpm - int(item['BPM'])), 100 - int(item['Popularity'])))
    return r

def findMatches(seed, bpm):
    seedId = getSeedId(seed)
    stuff = getOrderedBPMMatches(seedId, bpm)[0:5]
    print(json.dumps(stuff))


if __name__ == '__main__':
    findMatches("avicii the nights", 126)
