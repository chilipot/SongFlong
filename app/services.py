import logging
from pathlib import Path
from typing import List, Optional

from flask import current_app
from rq.job import Job

from app.songflong.download import VideoYTStreamDownloadAPI, AudioYTStreamDownloadAPI
from app.songflong.models import Song
from app.songflong.transcribe import setup_download_dir, generate_videos
from app.songflong.utils import QueueAPI

logger = logging.getLogger('songflong_builder')
logger.setLevel(logging.INFO)


class JobService:
    @classmethod
    def init_jobs(cls, primary_song: 'Song', secondary_songs: List['Song'] = None) -> Optional[List[int]]:
        download_dir = setup_download_dir()
        video_file = VideoYTStreamDownloadAPI().download(primary_song, download_dir)
        audio_test = AudioYTStreamDownloadAPI().download(primary_song, download_dir)
        if primary_song.video_artifact_file is None:
            logger.error(f"Cancelling request since no video stream could be found for {primary_song.video.url}")
            return None
        logger.info(f"Video Submission using {primary_song.video.url}: {video_file}")

        if secondary_songs is None:
            related_songs = []
            for related_song in primary_song.related_songs_by_tempo:
                try:
                    related_song.finish_loading()
                    related_songs.append(related_song)
                except Exception as e:
                    pass
            related_songs = related_songs[:5]  # Trim the list to just 5 songs to generate
        else:
            related_songs = secondary_songs

        jobs = []
        for related_song in related_songs:
            kwargs = {
                'download_dir': download_dir,
                'ffmpeg_path': Path(current_app.config.get("FFMPEG_PATH")),
                'song': related_song,
                'video_file_path': primary_song.video_artifact_file.file_path
            }

            job = QueueAPI.enqueue(generate_videos, **kwargs)
            jobs.append(job.get_id())
        return jobs

    @classmethod
    def get_job(cls, job_id: int) -> Job:
        return QueueAPI.get(job_id)
