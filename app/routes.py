from flask import jsonify, Blueprint, send_from_directory, current_app

from app.services import JobService

JOBS = Blueprint('jobs', __name__)


@JOBS.route('/ping')
def ping():
    return "pong", 200


@JOBS.route('/submit/<string:song_name>', methods=['POST'])
def submit(song_name):
    jobs = JobService.init_jobs(song_name)  # TODO: Actually Fix this
    if jobs:
        return jsonify(job_ids=jobs), 201
    else:
        return {'status', 'Unable to find video stream!'}, 424


@JOBS.route('/results/<string:job_id>')
def results(job_id):
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
