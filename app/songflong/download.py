import logging
import multiprocessing as mp
from abc import ABC
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial
from math import ceil
from pathlib import Path
from typing import Optional

import requests
from pytube import YouTube, Stream

from app.songflong.models import FileType

logger = logging.getLogger('songflong_builder')


class YTStreamDownloadAPI(ABC):
    BYTES_TO_MB = 2 ** 20
    DEFAULT_CHUNK_SIZE = 5 * BYTES_TO_MB

    def __init__(self, stream_type: FileType):
        self.stream_type = stream_type

    def download(self, song: 'Song', download_dir: Path) -> Path:
        """
        Downloads a stream to a file from a YouTube link to the given directory.
        """
        try:
            logger.info(f"Downloading {self.stream_type.name.lower()} stream -> {song.video.url}")
            file_path = self.download_stream(song.video.url, download_dir)
            song.save_file(file_path, self.stream_type)
            return file_path
        except Exception as err:
            logger.error(f"Unable to find an {self.stream_type.name.lower()} stream -> {song.video.url}")
            logger.exception(err)

    def get_stream(self, video_url: str) -> Optional[Stream]:
        stream_query = YouTube(video_url).streams.filter(adaptive=True)
        if self.stream_type is FileType.AUDIO_ARTIFACT:
            return stream_query.get_audio_only()
        elif self.stream_type is FileType.VIDEO_ARTIFACT:
            return stream_query.filter(only_video=True, subtype='mp4').order_by('resolution').desc().first()
        else:
            return None

    def download_stream(self, yt_url: str, download_dir: Path) -> Path:
        """
        Downloads the stream for the given youtube URL by separating it into multiple chunks.
        """
        stream = self.get_stream(yt_url)
        filename = download_dir / f"{stream.default_filename}-{self.stream_type}"
        url = stream.url
        filesize = stream.filesize

        ranges = [[url, i * self.DEFAULT_CHUNK_SIZE, (i + 1) * self.DEFAULT_CHUNK_SIZE - 1]
                  for i in range(ceil(filesize / self.DEFAULT_CHUNK_SIZE))]
        # Last range must be to the end of file, so it will be marked as None.
        ranges[-1][2] = None
        args = zip(*ranges)
        with ThreadPoolExecutor() as pool:
            chunks = pool.map(self.download_chunk, *args)

        with open(filename, 'wb') as outfile:
            for chunk in chunks:
                outfile.write(chunk)
        return Path(filename)

    @staticmethod
    def download_chunk(url: str, start: int, finish: int = None) -> bytes:
        """
        Requests a chunk of the file to be downloaded.
        """
        range_string = f"{start}-{finish if finish is not None else ''}"
        response = requests.get(url, headers={'Range': 'bytes=' + range_string})
        return response.content


class AudioYTStreamDownloadAPI(YTStreamDownloadAPI):
    def __init__(self):
        super().__init__(FileType.AUDIO_ARTIFACT)


class VideoYTStreamDownloadAPI(YTStreamDownloadAPI):
    def __init__(self):
        super().__init__(FileType.VIDEO_ARTIFACT)
