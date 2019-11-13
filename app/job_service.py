import logging
from typing import List

from flask import current_app

from app.songflong.download import download_video_stream
from app.songflong.links import video_links
from app.songflong.transcribe import setup_download_dir, generate_videos

logger = logging.getLogger('songflong_builder')
logger.setLevel(logging.INFO)


def setup_jobs(song_name: str) -> List[int]:
    download_dir = setup_download_dir()
    video_link, similar_links = video_links(song_name)
    video_file = download_video_stream(video_link, download_dir)
    if video_file is None:
        logger.error(f"Cancelling request since no video stream could be found for {video_link}")
        return None
    logger.info(f"Video Submission using {video_link}:{video_file}")
    jobs = []
    for song, link in similar_links:
        job = current_app.q.enqueue(generate_videos,
                                    str(video_file),
                                    link,
                                    str(download_dir),
                                    current_app.config.get("FFMPEG_PATH"),
                                    **song)
        jobs.append(job.get_id())
    return jobs


def get_job(job_id: int):
    return current_app.q.fetch_job(job_id)
