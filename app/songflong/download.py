from pytube import YouTube
from pathlib import Path
import multiprocessing as mp
from math import ceil
import requests
import logging

logger = logging.getLogger('songflong_builder')


def download_stream(video_url: str, itag: int, download_dir: Path):
    """
    Downloads the stream by separating it into multiple chunks.

    :param video_url: The YouTube link
    :param itag: YouTube's stream format code
    :param download_dir: The Path of the download directory
    """
    CHUNK_SIZE = 3 * 2**20  # bytes
    stream = YouTube(video_url).streams.get_by_itag(itag)
    filename = download_dir / f"{stream.type}-{stream.default_filename}.mp4"
    url = stream.url
    filesize = stream.filesize

    ranges = [[url, i * CHUNK_SIZE, (i + 1) * CHUNK_SIZE - 1]
              for i in range(ceil(filesize / CHUNK_SIZE))]
    # Last range must be to the end of file, so it will be marked as None.
    ranges[-1][2] = None

    pool = mp.Pool(min(len(ranges), 64))
    chunks = pool.map(download_chunk, ranges)

    with open(filename, 'wb') as outfile:
        for chunk in chunks:
            outfile.write(chunk)
    return Path(filename)


def download_chunk(args):
    """
    Requests a chunk of the file to be downloaded.

    :param args: The chunk start and finish
    :type args: tuple
    :returns: The data from the get request
    """
    url, start, finish = args
    range_string = '{}-'.format(start)

    if finish is not None:
        range_string += str(finish)

    response = requests.get(url, headers={'Range': 'bytes=' + range_string})
    return response.content


def download_audio_stream(url: str, download_dir: Path) -> Path:
    """
    Downloads the audio of the YouTube link to the given directory.

    :param url: A YouTube link
    :type url: str
    :param download_dir: The directory to download the stream to
    :type download_dir: Path
    :returns: The Path of the downloaded audio stream
    :rtype: Path
    """

    try:
        logger.info(f"Downloading audio stream -> {url}")
        return download_stream(url, 140, download_dir)
    except Exception as err:
        logger.error(f"Unable to find an audio stream for {url}")
        logger.exception(err)


def download_video_stream(url: str, download_dir: Path) -> Path:
    """
    Downloads the video of the YouTube link to the given directory.

    :param url: A YouTube link
    :type url: str
    :param download_dir: The directory to download the stream to
    :type download_dir: Path
    :returns: The Path of the downloaded video stream
    :rtype: Path
    """

    try:
        logger.info(f"Downloading video stream -> {url}")
        return download_stream(url, 135, download_dir)
    except Exception as err:
        logger.error(f"Unable to find an video stream for {url}")
        logger.exception(err)
