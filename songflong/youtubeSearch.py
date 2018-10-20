from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import json
from .download import run as downloadFromLinks
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from .video import VideoData

DEVELOPER_KEY = "AIzaSyCUqAGy-BkcxGU0QZqVSPsxrnAvkWK6CUo"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"




def youtube_search(q, max_results=5,order="relevance", token=None, location=None, location_radius=None):

  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet",
    maxResults=max_results,
    location=location,
    locationRadius=location_radius

  ).execute()



  videos = []

  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append(search_result)
  try:
      nexttok = search_response["nextPageToken"]
      return(nexttok, videos)
  except Exception as e:
      nexttok = "last_page"
      return(nexttok, videos)


def geo_query(video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    video_response = youtube.videos().list(
        id=video_id,
        part='snippet, recordingDetails, statistics'

    ).execute()

    return video_response

def getAudioLink(video):
    title = video.keywords
    nt, res = youtube_search(title + ' audio')
    try:
        videoId = res[0]['id']['videoId']
        video.url = 'https://www.youtube.com/watch?v=%s' % videoId
        return video
    except:
        print("No Video Found... Search Failed")

def findAllLinks(video):
    pool = ThreadPool(5)
    results = pool.map(getAudioLink, video)
    pool.close()
    pool.join()
    return list(results)

if __name__ == '__main__':
    print(getAudioLink("guns and roses paradise city"))
    print(findAllLinks(['Crescerai Nomadi', 'Come Sei Bella Massimo Di Cataldo', 'Io vagabondo (che non sono altro) Nomadi', 'Hey - Original Mix Nightriders']))
