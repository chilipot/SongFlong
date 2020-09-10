import logging
import subprocess
from pathlib import Path

logger = logging.getLogger('songflong_builder')


def ffmpeg_merge_video_audio(video: Path, audio: Path, output: Path, ffmpeg_path: str):
    """
    Merges video and audio files into a single movie file.

    :param video: The Path to the video file
    :param audio: The Path to the audio file
    :param output: The destination Path for the merged movie file
    :param ffmpeg_path: The str path to ffmpeg executable
    """

    cmd = [ffmpeg_path, "-y", "-i", str(audio), "-i", str(video),
           "-vcodec", 'copy', "-acodec", 'copy', str(output)]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, )
        if proc.returncode:
            raise IOError(proc.stderr)
        else:
            logger.info('FFMPEG - Command successful')
    except Exception as err:
        logger.warning(f"Merging audio:{str(audio)} and video:{str(video)} to output{str(output)}")
        logger.error(err)
