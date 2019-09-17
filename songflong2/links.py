from googleapiclient import discovery

DEVELOPER_KEY = "AIzaSyCUqAGy-BkcxGU0QZqVSPsxrnAvkWK6CUo"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(query: str) -> list:
    """
    Returns a list of the most relevent videos.

    :param query: The search query
    :type query: str
    :returns: A list of relevant YouTube video links
    :rtype: list
    """

    youtube = discovery.build(YOUTUBE_API_SERVICE_NAME,
                              YOUTUBE_API_VERSION,
                              developerKey=DEVELOPER_KEY)

    # Query for 3 results just in case a video is weird
    search_response = youtube.search().list(
        q=query,
        type="video",
        pageToken=None,
        order="relevance",
        part="id,snippet",
        maxResults=3,
        location=None,
        locationRadius=None
    ).execute()

    return [search_result for search_result
            in search_response.get("items", [])
            if search_result["id"]["kind"] == "youtube#video"]

def getYouTubeLink(title: str) -> list:
    """
    Searches YouTube and builds a link to the most relevant video.

    :param title: The title of the song
    :type title: str
    :returns: A YouTube link
    :rtype: str
    """

    res = youtube_search(title + ' audio')
    try:
        return f"https://www.youtube.com/watch?v={res[0]['id']['videoId']}"
    except IndexError or KeyError:
        print("No Video Found... Search Failed")

def findAllLinks(titles: list) -> list:
    """
    Returns the YouTube links of the given song titles.

    :param videos: A list of song titles
    :type videos: list
    :returns: A list of YouTube links
    :rtype: list
    """

    return [getYouTubeLink(title) for title in titles]


if __name__ == '__main__':
    # print(getYouTubeLink("guns and roses paradise city"getYouTubeLink))
    # print(findAllLinks(['Crescerai Nomadi', 'Come Sei Bella Massimo Di Cataldo',
    #                     'Io vagabondo (che non sono altro) Nomadi', 'Hey - Original Mix Nightriders']))

    from search import getSongsByBPM, getTrackTuneBatBPM

    song_input = "All Day and all of the night"
    bpm = getTrackTuneBatBPM(song_input)
    songs = getSongsByBPM(bpm)
    # print(songs)
    print(f"{song_input} - {getYouTubeLink(song_input)}")
    print([f"{song} - {link}" for song, link in zip(songs, findAllLinks(songs))])
    print([(song, link) for song, link in zip(songs, findAllLinks(songs))])
