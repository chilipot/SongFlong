import uuid
import os

class User:
    def __init__(self, ytURL, data=[]*5):
        self.uuid = str(uuid.uuid4())
        self.downloadPath = os.getcwd() + '\\app\\static\\' + self.uuid
        self.ytURL = ytURL
        self.data = data
        try:
            os.mkdir(self.downloadPath)
            os.mkdir(self.downloadPath + r'\tmp')
            os.mkdir(self.downloadPath + r'\output')
        except OSError:
            print("Failed to create directory")
