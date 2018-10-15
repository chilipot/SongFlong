import os
from video import VideoData
from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio

videoclip = None

def combineAV(data):
    audioPath = data.tempLoc
    downloadPath = os.getcwd() + r'\app\static\output'
    print(audioPath)

    pathSplit = audioPath.split("\\")
    print(pathSplit)
    name = pathSplit[-1]
    print(name)
    data.final = 'static/output/video' + name
    output = 'app\static\output\\video' + name
    print(audioPath)
    ffmpeg_merge_video_audio(videoclip, audioPath, output, vcodec='copy', acodec='copy', ffmpeg_output=True, verbose=True)

    print(data.final)

    os.remove(audioPath)
    return output

def createVideoFiles(files):
    print(files)
    global videoclip
    videoclip = files[0].tempLoc

    print(files[1:])
    results = list(map(lambda file: combineAV(file), files[1:]))


    print("done")
    results = list(map(lambda file: 'output/' + file, results))
    print(os.getcwd())
    print(results)
    os.remove(videoclip)
    return results

if __name__ == '__main__':
    audioclip = VideoData(url="", title="Test", keywords="", tempLoc=r"C:\Users\dangu\OneDrive\Computer Files\Documents\GitHub\Sound-Repo-Thing\tmp\audioAvicii - Levelsmp4.mp4")
    videoclip = r"C:\Users\dangu\OneDrive\Computer Files\Documents\GitHub\Sound-Repo-Thing\tmp\videoAvicii - Levelsmp4.mp4"
    print(audioclip)
    combineAV(audioclip)
    print('done')
