from moviepy.editor import *
import os

videoclip = None

def combineAV(audioPath):
    downloadPath = os.getcwd() + r'\app\static\output'
    print(audioPath)
    audioclip = AudioFileClip(audioPath)
    final = videoclip.set_audio(audioclip)

    pathSplit = audioPath.split("\\")
    print(pathSplit)
    name = pathSplit[-1]
    print(name)
    final.write_videofile(downloadPath + r'\video' + name, threads=8, preset='ultrafast')
    return 'video' + name

def createVideoFiles(files):
    print(files)
    global videoclip
    videoclip = VideoFileClip(files['video'])

    print(files['audio'])
    results = list(map(lambda file: combineAV(file), files['audio']))


    print("done")
    results = list(map(lambda file: 'output/' + file, results))
    print(os.getcwd())
    print(results)
    return results

if __name__ == '__main__':
    createVideoFiles({'video': 'C:\\Users\\dangu\\OneDrive\\Computer Files\\Documents\\GitHub\\Sound-Repo-Thing\\tmp\\videoAvicii - Levelsmp4.mp4', 'audio': 'C:\\Users\\dangu\\OneDrive\\Computer Files\\Documents\\GitHub\\Sound-Repo-Thing\\tmp\\audioMike Williams - Give It Up (Audio)mp4.mp4'})
