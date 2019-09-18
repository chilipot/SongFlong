import urllib.parse
import urllib.request
from bs4 import BeautifulSoup


def youtube_search(query: str) -> list:
    """
    Returns a list of the most relevant videos.

    :param query: The search query
    :type query: str
    :returns: A list of relevant YouTube video links
    :rtype: list
    """
    vid_links = []

    # Video Filter param + query
    params = {"sp": urllib.parse.unquote("EgIQAQ%253D%253D"), "search_query": query}

    url = f"https://www.youtube.com/results?{urllib.parse.urlencode(params)}"

    response = urllib.request.urlopen(url)

    soup = BeautifulSoup(response.read(), 'html.parser')

    # Get links from top 3 results
    for vid in soup.find_all(class_="yt-uix-tile-link")[:3]:
        href = vid["href"].split('&')[0]
        print(href)
        if href.startswith("/watch?v="):
            vid_links.append(href)
    return vid_links


def get_youtube_link(title: str, is_audio=True) -> list:
    """
    Searches YouTube and builds a link to the most relevant video.

    :param title: The title of the song
    :type title: str
    :param is_audio: Whether link should be primarily audio (video doesn't matter)
    :type is_audio: bool
    :returns: A YouTube link
    :rtype: str
    """

    links = youtube_search(f"{title}{' audio' if is_audio else ''}")

    try:
        return f"https://www.youtube.com{links[0]}"
    except IndexError or KeyError:
        print("No Video Found... Search Failed")


def find_all_links(titles: list, is_audio=True) -> list:
    """
    Returns the YouTube links of the given song titles.

    :param titles: A list of song titles
    :type titles: list
    :param is_audio: Whether links should be primarily audio links (video doesn't matter)
    :type is_audio: bool
    :returns: A list of YouTube links
    :rtype: list
    """

    return [get_youtube_link(title, is_audio) for title in titles]


if __name__ == '__main__':
    # print(getYouTubeLink("guns and roses paradise city"getYouTubeLink))
    # print(findAllLinks(['Crescerai Nomadi', 'Come Sei Bella Massimo Di Cataldo',
    #                     'Io vagabondo (che non sono altro) Nomadi', 'Hey - Original Mix Nightriders']))

    from search import getSongsByBPM, getTrackTuneBatBPM

    song_input = "All Day and all of the night"
    bpm = getTrackTuneBatBPM(song_input)
    songs = getSongsByBPM(bpm)
    # print(songs)
    print(f"{song_input} - {get_youtube_link(song_input)}")
    print([f"{song} - {link}" for song,
           link in zip(songs, find_all_links(songs))])
    print([(song, link) for song, link in zip(songs, find_all_links(songs))])
