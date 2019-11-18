import uuid
from pathlib import Path

from app.songflong.download import download_audio_stream
from app.songflong.ffmpeg import ffmpeg_merge_video_audio


def setup_download_dir():
    download_dir = Path('temp')
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir


def transcribe_video(video_file: Path, audio_file: Path, download_dir: Path, ffmpeg_path: str) -> Path:
    """
    Transcribes the audio to the video and outputs a file.

    :param ffmpeg_path: FFMPEG PATH
    :type ffmpeg_path: str
    :param video_file: The base video stream
    :type video_file: Path
    :param audio_file: The downloaded audio stream
    :type audio_file: Path
    :param download_dir: The session directory
    :type download_dir: Path
    """
    output = download_dir / f"output-{uuid.uuid4()}.mp4"
    ffmpeg_merge_video_audio(video_file, audio_file, output, ffmpeg_path)
    return output


def generate_videos(video_file, link, download_dir, ffmpeg_path, **kwargs):
    download_dir = Path(download_dir)
    video_file = Path(video_file)
    audio_file = download_audio_stream(link, download_dir)
    finished_video = transcribe_video(video_file, audio_file, download_dir, ffmpeg_path)
    print(f"******FINISHED TRANSCRIBING*****")
    return {"filepath": str(finished_video.name), **kwargs}
