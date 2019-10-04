import uuid
from pathlib import Path

from app.songflong.download import download_audio_stream
from app.songflong.ffmpeg import ffmpeg_merge_video_audio


def setup_download_dir():
    download_dir = Path('temp')
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir


def transcribe_video(video_file: Path, audio_file: Path, download_dir: Path) -> Path:
    """
    Transcribes the audio to the video and outputs a file.

    :param video_file: The base video stream
    :type video_file: Path
    :param audio_file: The downloaded audio stream
    :type audio_file: Path
    :param download_dir: The session directory
    :type download_dir: Path
    """
    output = download_dir / f"output-{uuid.uuid4()}.mp4"
    ffmpeg_merge_video_audio(video_file, audio_file, output)
    return output


def generate_videos(video_file, title, link, download_dir):
    audio_file = download_audio_stream(link, download_dir)
    finished_video = transcribe_video(video_file, audio_file, download_dir)
    print(f"******FINISHED TRANSCRIBING*****")
    return finished_video
