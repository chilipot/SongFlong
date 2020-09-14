import logging
import subprocess
import uuid
from pathlib import Path

from app.songflong.download import AudioYTStreamDownloadAPI
from app.songflong.models import FileType

logger = logging.getLogger('songflong_builder')


def setup_download_dir():
    download_dir = Path('temp')
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir


def ffmpeg_merge_video_audio(video: Path, audio: Path, output: Path, ffmpeg_path: Path):
    """
    Merges video and audio files into a single movie file.

    :param video: The Path to the video file
    :param audio: The Path to the audio file
    :param output: The destination Path for the merged movie file
    :param ffmpeg_path: The str path to ffmpeg executable
    """

    cmd = [str(ffmpeg_path), "-y", "-i", str(audio), "-i", str(video),
           "-vcodec", 'copy', "-acodec", 'copy', str(output)]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode:
            raise IOError(proc.stderr)
        else:
            logger.info('FFMPEG - Command successful')
    except Exception as err:
        logger.warning(f"Merging audio:{str(audio)} and video:{str(video)} to output{str(output)}")
        logger.error(err)


def transcribe_video(video_file: Path, audio_file: Path, download_dir: Path, ffmpeg_path: Path) -> Path:
    """
    Transcribes the audio to the video and outputs a file.

    :param ffmpeg_path: FFMPEG PATH
    :param video_file: The base video stream
    :param audio_file: The downloaded audio stream
    :param download_dir: The session directory
    """
    output = download_dir / f"output-{uuid.uuid4()}.mp4"
    ffmpeg_merge_video_audio(video_file, audio_file, output, ffmpeg_path)
    return output


def generate_videos(song: 'Song', download_dir: Path, ffmpeg_path: Path):
    download_dir = Path(download_dir)
    video_file = Path(song.video.video_artifact_file)
    audio_file_path = AudioYTStreamDownloadAPI().download(song, download_dir)
    finished_video = transcribe_video(video_file, audio_file_path, download_dir, ffmpeg_path)
    song.save_file(finished_video, FileType.GENERATED_VIDEO)

    print(f"******FINISHED TRANSCRIBING*****")
    return {"song": song.serialize()}
