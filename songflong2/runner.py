import logging
import os
from queue import Queue
from threading import Thread
from time import time, sleep
from tempfile import TemporaryFile
from search import get_songs_by_bpm, get_track_bpm
from links import get_youtube_link, find_all_links
import json
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen, Request
from download import download_video_stream, download_audio_stream
from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio


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

    return (get_youtube_link(initial_song), [(song, link) for song, link in zip(songs, find_all_links(songs))])


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
    # ffmpeg_merge_video_audio(video_file, audio_file, download_dir, vcodec='copy', acodec='copy', ffmpeg_output=True)
    pass


class VideoWorker(Thread):
    """Pulls link from the Queue and downloads it"""

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue: Queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            video_file, title, link, download_dir = self.queue.get()
            try:
                audio_file = download_audio_stream(link, download_dir)
                transcribe_video(video_file, audio_file, download_dir)
            finally:
                self.queue.task_done()


class DownloadQueue():
    """A Queue to hold download links and spawns workers"""

    @classmethod
    def _spawn_worker(cls, queue: Queue):
        """
        Spawns a new worker daemon

        :param queue: The shared memory space to grab tasks from
        :type queue: Queue
        """

        worker = VideoWorker(queue)
        worker.daemon = True
        worker.start()

    def __init__(self, count: int = 2):
        self.count: int = count
        self.queue: Queue = Queue()

        for x in range(count):
            self._spawn_worker(self.queue)

    def add_links(self, links: list, video_file: Path, download_dir: Path):
        """
        Adds a list of links to the download queue

        :param links: A list of tuples containing the YouTube video metadata
        :type links: list
        :param video_file: The file containing the Video stream
        :type video_file: Path
        """

        for title, link in links:
            logger.info(f"Queueing Link -> {title} '{link}'")
            self.queue.put((video_file, title, link, download_dir))

    def close(self):
        """Waits until all the items in the queue are processed before closing"""
        self.queue.join()


if __name__ == '__main__':
    ts = time()
    download_dir = setup_download_dir()
    video_link, similar_links = video_links(
        "All Day and all of the night")  # Demo
    video_file = download_video_stream(video_link, download_dir)
    pipeline = DownloadQueue(count=8)
    pipeline.add_links(similar_links, video_file, download_dir)
    pipeline.close()
    logging.info('Took %s', time() - ts)
