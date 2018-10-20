
from flask import Flask
from config import Config
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app)

from app import routes

if __name__ == '__main__':
    socketio.run(app)
