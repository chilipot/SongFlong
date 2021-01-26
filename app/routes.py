import jsonpickle
from flask import jsonify, Blueprint, send_from_directory, current_app, request

from app.services import JobService
from app.songflong.models import Song
from app.songflong.utils import responsify

JOBS = Blueprint('jobs', __name__)


@JOBS.route('/ping')
def ping():
    return "pong", 200


@JOBS.route('/search')
def search():
    query = request.args.get('query', None, str)
    query = query.strip()
    if not query:
        return jsonify([]), 202
    else:
        results = Song.search(query, fully_loaded=True)
        return responsify({"results": results}), 200


@JOBS.route('/related', methods=['POST'])
def lookup_related_by_tempo():
    serialized_in_song = str(request.data, encoding='utf-8')
    song = Song.deserialize(serialized_in_song)
    related_songs = []
    for related_song in song.related_songs_by_tempo:
        try:
            related_song.finish_loading()
            related_songs.append(related_song)
        except Exception as e:
            pass
    return responsify({"results": related_songs})


@JOBS.route('/submit/', methods=['POST'])
def submit():
    serialized_in_songs = str(request.data, encoding='utf-8')
    in_songs = jsonpickle.decode(serialized_in_songs)
    jobs = JobService.init_jobs(in_songs["primary"], in_songs.get("secondary"))
    if jobs:
        return jsonify(job_ids=jobs), 201
    else:
        return {'status', 'Unable to find video stream!'}, 424


@JOBS.route('/results/<string:job_id>')
def job_results(job_id):
    job = JobService.get_job(job_id)

    if job.is_failed:
        return {'status': 'Job has failed!'}, 400

    if job.is_finished:
        return jsonify(job.result)

    return {'status': 'Job has not finished!'}, 202


@JOBS.route('/video/<string:video_path>')
def get_video(video_path):
    # Serve directly from a better web server
    return send_from_directory(directory=current_app.static_folder, filename=video_path)
