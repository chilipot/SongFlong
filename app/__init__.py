import os

from flask import Flask
from redis import StrictRedis
from rq import Queue


def create_app():
    app = Flask(__name__, static_folder="../temp")
    app.config["FFMPEG_PATH"] = os.environ.get("FFMPEG_PATH", default="/usr/bin/ffmpeg")
    app.q = Queue(connection=StrictRedis())
    from app.routes import JOBS
    app.register_blueprint(JOBS)
    return app
