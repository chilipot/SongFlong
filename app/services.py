import logging
from pathlib import Path
from typing import List, Optional

from flask import current_app
from rq.job import Job

from app.songflong.download import VideoYTStreamDownloadAPI
from app.songflong.transcribe import setup_download_dir, generate_videos
from app.songflong.utils import QueueAPI

logger = logging.getLogger('songflong_builder')
logger.setLevel(logging.INFO)


class JobService:
    @classmethod
    def init_jobs(cls, song: 'Song') -> Optional[List[int]]:
        download_dir = setup_download_dir()
        video_file = VideoYTStreamDownloadAPI().download(song, download_dir)
        if song.video.video_artifact_file is None:
            logger.error(f"Cancelling request since no video stream could be found for {song.video.url}")
            return None
        logger.info(f"Video Submission using {song.video.url}: {video_file}")
        jobs = []
        for related_song in song.related_songs_by_tempo:
            kwargs = {
                'download_dir': download_dir,
                'ffmpeg_path': Path(current_app.config.get("FFMPEG_PATH")),
                'song': related_song
            }
            job = QueueAPI.enqueue(generate_videos, **kwargs)
            jobs.append(job.get_id())
        return jobs

    @classmethod
    def get_job(cls, job_id: int) -> Job:
        return current_app.q.fetch_job(job_id)
