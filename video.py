import pytube

class VideoData:
    def __init__(self,keywords, title, url=None, spotify=None, stream=None, tempLoc=None, final=None):
        self.title = title
        self.url = url
        self.spotify = spotify
        self.stream = stream
        self.tempLoc = tempLoc
        self.final = final
        self.keywords = keywords

    def __repr__(self):
        return 'data' + self.keywords
