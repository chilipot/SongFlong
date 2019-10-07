import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

from app.songflong.bpm_search import get_track_bpm, get_songs_by_bpm


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
        if href.startswith("/watch?v="):
            vid_links.append(href)
    return vid_links


def get_youtube_link(title: str, is_audio=True) -> str:
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


def video_links(initial_song: str) -> tuple:
    """
    Finds a list of songs with similar BPM to the given query song.

    :param initial_song: The title of the given song
    :type initial_song: str
    :returns: Tuple of the original link and list of tuples containing the song title, author, and YouTube link
        of similar songs
    :rtype: tuple
    """
    bpm = get_track_bpm(initial_song)
    songs = get_songs_by_bpm(bpm)
    song_titles = [song["title"] for song in songs]

    return get_youtube_link(initial_song, is_audio=False), \
           [(song, link) for song, link in zip(songs, find_all_links(song_titles))]
