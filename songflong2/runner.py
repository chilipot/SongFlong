import logging
import os
from queue import Queue
from threading import Thread
from time import time, sleep
from tempfile import TemporaryFile
from search import getSongsByBPM, getTrackTuneBatBPM
from links import getYouTubeLink, findAllLinks
import json
from pathlib import Path
from urllib.request import urlopen, Request

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
    bpm = getTrackTuneBatBPM(initial_song)
    songs = getSongsByBPM(bpm)

    # print(f"{initial_song} - {getYouTubeLink(initial_song)}")
    return [(song, link) for song, link in zip(songs, findAllLinks(songs))]


def setup_download_dir():
    download_dir = Path('temp')
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir


class VideoWorker(Thread):
    """Pulls link from the Queue and downloads it"""

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue: Queue = queue

    @staticmethod
    def download_link(directory, link):
        # TODO: Replace this with the actual downloading part
        download_path = directory / os.path.basename(link)
        with urlopen(link) as video, download_path.open('wb') as f:
            # at the moment this downloads the HTML page and names the files as the param in
            f.write(video.read())
        logger.info('Downloaded %s', link)
        return link

    def transcribe_video():

        pass

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            directory, title, link = self.queue.get()
            try:
                foo = self.download_link(directory, link)
                print(foo)
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

    def add_links(self, links: list, download_dir: Path):
        """
        Adds a list of links to the download queue

        :param links: A list of tuples containing the YouTube video metadata
        :type links: list
        :param download_dir: The directory to download the YouTube files
        :type download_dir: Path
        """

        for title, link in links:
            logger.info(f"Queueing Link -> {title} '{link}'")
            self.queue.put((download_dir, title, link))

    def close(self):
        """Waits until all the items in the queue are processed before closing"""
        self.queue.join()


def main():
    ts = time()
    download_dir = setup_download_dir()
    links = video_links("All Day and all of the night")  # Demo

    pipeline = DownloadQueue(count=8)
    pipeline.add_links(links, download_dir)
    pipeline.close()
    logging.info('Took %s', time() - ts)


if __name__ == '__main__':
    main()
