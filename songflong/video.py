import pytube
from .complex_json_encoder import *

class VideoData(ComplexJSONSerializable):
    def __init__(self,keywords, title, url=None, art=None, artist=None, stream=None, tempLoc=None, final=None):
        self.title = title
        self.url = url
        self.art = art
        self.stream = stream
        self.artist = artist
        self.tempLoc = tempLoc
        self.final = final
        self.keywords = keywords

    def __repr__(self):
        return 'data' + self.keywords
