#convert mp3 to wav

from pydub import AudioSegment

sound = AudioSegment.from_mp3("\Users\Skyler\Sound-Repo-Thingfile\Avicii.mp3")
sound.export("/Users/Skyler/Sound-Repo-Thingfile/file.wav", format="wav")
