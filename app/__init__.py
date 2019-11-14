import os

from flask import Flask
from flask_cors import CORS
from redis import StrictRedis
from rq import Queue


def create_app():
    app = Flask(__name__, static_folder="../temp")
    CORS(app)
    app.config["FFMPEG_PATH"] = os.environ.get(
        "FFMPEG_PATH", default="/usr/bin/ffmpeg")
    app.q = Queue(connection=StrictRedis(host='redis', port='6379'))
    from app.routes import JOBS
    app.register_blueprint(JOBS)
    return app
