import requests
import json
import urllib

def getSeedId(query):
    encodedQueryString = urllib.parse.urlencode({'query' : query, 'queryType': 'track'})
    url = "https://tunebat.com/Advanced/SeedQuery?" + encodedQueryString
    r = requests.get(url).json()['TrackItems'][0]['Id']
    #print(r)
    return r

def getOrderedBPMMatches(bpm, seedId=""):
    minBPMStr = str(bpm - 5)
    maxBPMStr = str(bpm + 5)
    seedIdStr = "[]" if seedId == "" else "[%22" + seedID + "%22]"
    url = "https://tunebat.com/Advanced/AdvancedQuery?inputs={%22Target%22:{%22DurationMs%22:null,%22Energy%22:null,%22Danceability%22:null,%22Valence%22:null,%22Loudness%22:null,%22Acousticness%22:null,%22Instrumentalness%22:null,%22Liveness%22:null,%22Speechiness%22:null},%22Min%22:{%22Tempo%22:" + minBPMStr + ",%22Popularity%22:30},%22Max%22:{%22Tempo%22:" + maxBPMStr + ",%22Popularity%22:100},%22TrackSeeds%22:" + seedIdStr + ",%22ArtistSeeds%22:[]}"
    r = requests.get(url).json()['TrackItems']
    #print(json.dumps(r[0:2]))
    r.sort(key=lambda item : (abs(bpm - int(item['BPM'])), 100 - int(item['Popularity'])))
    #print(json.dumps(r[0:2]))
    return r

    
if __name__ == '__main__':
    seedId = getSeedId("avicii the nights")
    stuff = getOrderedBPMMatches(126, "")[0:5]
    print(stuff)
    
