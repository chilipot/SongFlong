import logging
import uuid
from pathlib import Path
from queue import Queue
from threading import Thread
from time import time

from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio

from .download import download_video_stream, download_audio_stream
from .links import get_youtube_link, find_all_links
from .search import get_songs_by_bpm, get_track_bpm

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def video_links(initial_song):
    """
    Finds a list of songs with similar BPM to the given query song.

    :param initial_song: The title of the given song
    :type initial_song: str
    :returns: A list of tuples containing the song title, author, and YouTube link
    :rtype: list
    """
    bpm = get_track_bpm(initial_song)
    songs = get_songs_by_bpm(bpm)

    return get_youtube_link(initial_song, is_audio=False), \
        [(song, link) for song, link in zip(songs, find_all_links(songs))]


def setup_download_dir():
    download_dir = Path('temp')
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir


def transcribe_video(video_file: Path, audio_file: Path, download_dir: Path):
    """
    Transcribes the audio to the video and outputs a file.

    :param video_file: The base video stream
    :type video_file: Path
    :param audio_file: The downloaded audio stream
    :type audio_file: Path
    :param download_dir: The session directory
    :type download_dir: Path
    """
    output = download_dir / f"output-{uuid.uuid4()}.mp4"
    ffmpeg_merge_video_audio(str(video_file), str(audio_file), str(output),
                             vcodec='copy', acodec='copy', ffmpeg_output=True)
    return output


def generate_videos(video_file, title, link, download_dir):
    audio_file = download_audio_stream(link, download_dir)
    finished_video = transcribe_video(video_file, audio_file, download_dir)
    print(f"******FINISHED TRANSCRIBING*****")
    return finished_video
