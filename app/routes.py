from flask import jsonify, send_file, Blueprint

from app import job_service

JOBS = Blueprint('jobs', __name__)


@JOBS.route('/')
def index():
    return "Hello, World!", 200


@JOBS.route('/submit/<string:song_name>')
def submit(song_name):
    jobs = job_service.setup_jobs(song_name)
    return jsonify(job_ids=jobs)


@JOBS.route('/results/<string:job_id>')
def results(job_id):
    job = job_service.get_job(job_id)

    if job.is_failed:
        return 'Job has failed!', 400

    if job.is_finished:
        return send_file(filename_or_fp=str(job.result.absolute()))

    return 'Job has not finished!', 202
