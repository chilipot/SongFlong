from flask import Flask, jsonify, request
from redis import StrictRedis
from rq import Queue
from songflong2.runner import setup_download_dir, video_links, download_video_stream, generate_videos

from random import randrange


app = Flask(__name__)

q = Queue(connection=StrictRedis())


@app.route('/')
def get_randrange():

    if 'stop' in request.args:

        stop = int(request.args.get('stop'))
        start = int(request.args.get('start', 0))
        step = int(request.args.get('step', 1))

        job = q.enqueue(randrange, start, stop, step, result_ttl=5000)

        return jsonify(job_id=job.get_id())

    return 'Stop value not specified!', 400

@app.route('/video/<string:song_name>')
def generate_videos(song_name):
    download_dir = setup_download_dir()
    video_link, similar_links = video_links(song_name)
    video_file = download_video_stream(video_link, download_dir)
    jobs = []
    for title, link in similar_links:
        job = q.enqueue(generate_videos, video_file, title, link, download_dir)
        jobs.append(job.get_id())

    return jsonify(job_ids=jobs)

@app.route("/results")
@app.route("/results/<string:job_id>")
def get_results(job_id=None):

    if job_id is None:
        return jsonify(queued_job_ids=q.job_ids)

    job = q.fetch_job(job_id)

    if job.is_failed:
        return 'Job has failed!', 400

    if job.is_finished:
        return jsonify(result=job.result)

    return 'Job has not finished!', 202

if __name__ == '__main__':
    # Start server
    app.run(host='0.0.0.0', port=8080, debug=True)
