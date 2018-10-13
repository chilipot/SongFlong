from moviepy.editor import *
import os

downloadPath = os.getcwd() + r'\tmp'
audioclip = AudioFileClip(downloadPath + r'\originala1.mp4')
videoclip = VideoFileClip(downloadPath + r'\originalv2.mp4')

final = videoclip.set_audio(audioclip)

final.write_videofile(downloadPath + r'\final.mp4')

print("done")
