from flask import Flask, jsonify, request, send_file
from redis import StrictRedis
from rq import Queue
from .songflong import setup_download_dir, video_links, download_video_stream, generate_videos


app = Flask(__name__)

q = Queue(connection=StrictRedis())


@app.route('/')
def index():

    return "Hello, World!", 200

    return 'Stop value not specified!', 400

@app.route('/submit/<string:song_name>')
def submit(song_name):
    download_dir = setup_download_dir()
    video_link, similar_links = video_links(song_name)
    video_file = download_video_stream(video_link, download_dir)
    jobs = []
    for title, link in similar_links:
        job = q.enqueue(generate_videos, video_file, title, link, download_dir)
        jobs.append(job.get_id())

    return jsonify(job_ids=jobs)

@app.route('/results/<string:job_id>')
def results(job_id):

    job = q.fetch_job(job_id)

    if job.is_failed:
        return 'Job has failed!', 400

    if job.is_finished:
        return send_file(filename_or_fp=str(job.result.absolute()))

    return 'Job has not finished!', 202

if __name__ == '__main__':
    # Start server

    app.run(host='0.0.0.0', port=8080, debug=True)
