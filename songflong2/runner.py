import logging
import os
from queue import Queue
from threading import Thread
from time import time
from tempfile import TemporaryFile
from search import getSongsByBPM, getTrackTuneBatBPM
from links import getYouTubeLink, findAllLinks
import json
from pathlib import Path
from urllib.request import urlopen, Request

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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
        self.queue = queue

    @staticmethod
    def download_link(directory, link):
        # TODO: Replace this with the actual downloading part
        download_path = directory / os.path.basename(link)
        with urlopen(link) as video, download_path.open('wb') as f:
            f.write(video.read()) # at the moment this downloads the HTML page and names the files as the param in
        logger.info('Downloaded %s', link)
        return link

    def transcribe_video():

        pass

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            directory, link = self.queue.get()
            try:
                foo = self.download_link(directory, link)
                print(foo)
            finally:
                self.queue.task_done()


def main():
    ts = time()
    download_dir = setup_download_dir()
    links = video_links("All Day and all of the night") # Demo
    # Create a queue to communicate with the worker threads
    queue = Queue()
    # Creates worker threads
    for x in range(8):
        worker = VideoWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue as a tuple
    for title, link in links:
        logger.info('Queueing {}'.format(link))
        queue.put((download_dir, link))
    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()
    logging.info('Took %s', time() - ts)

if __name__ == '__main__':
    main()
