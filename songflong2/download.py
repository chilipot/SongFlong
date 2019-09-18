from pytube import YouTube
from pathlib import Path
import logging
from time import time
from io import BytesIO

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def download_audio_stream(url: str, download_dir: Path) -> Path:
    """
    Downloads the audio of the YouTube link to the given directory.

    :param url: A YouTube link
    :type url: str
    :param downlaod_dir: The directory to download the stream to
    :type download_dir: Path
    :returns: The Path of the downloaded audio stream
    :rtype: Path
    """

    def bitrate(stream):
        return stream.abr in ['128kbps', '80kbps', '40kbps']

    youtube = YouTube(url)
    audio_stream = youtube.streams.filter(only_audio=True, subtype='mp4', adaptive=True, custom_filter_functions=[
                                          bitrate]).order_by('abr').desc().first()

    if audio_stream:
        logger.info(f"Downloading audio stream -> {url}")
        return audio_stream.download(output_path=download_dir, filename=audio_stream.type + audio_stream.default_filename)
    else:
        logger.error(f"Unable to find an audio stream for {url}")


def download_video_stream(url: str, download_dir: Path) -> Path:
    """
    Downloads the video of the YouTube link to the given directory.

    :param url: A YouTube link
    :type url: str
    :param downlaod_dir: The directory to download the stream to
    :type download_dir: Path
    :returns: The Path of the downloaded video stream
    :rtype: Path
    """

    def resolutions(stream):
        return stream.resolution in ['720p', '1080p', '480p', '360p', '240p', '144p']

    youtube = YouTube(url)
    video_stream = youtube.streams.filter(only_video=True, subtype='mp4', adaptive=True, custom_filter_functions=[
                                          resolutions]).order_by('resolution').desc().first()

    if video_stream:
        logger.info(f"Downloading video stream -> {url}")
        return video_stream.download(output_path=download_dir, filename=video_stream.type + video_stream.default_filename)
    else:
        logger.error(f"Unable to find an video stream for {url}")


if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=VYOjWnS4cMY'

    ts = time()
    download_audio_stream(url, Path('temp'))
    print('Took %s', time() - ts)
    ts = time()
    download_video_stream(url, Path('temp'))
    print('Took %s', time() - ts)
