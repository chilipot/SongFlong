from flask import Flask, jsonify, request
from redis import StrictRedis
from rq import Queue
from songflong2.runner import setup_download_dir, video_links, download_video_stream, generate_videos


app = Flask(__name__)

q = Queue(connection=StrictRedis())


@app.route('/')
def index():

    return "Hello, World!", 200

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


if __name__ == '__main__':
    # Start server
    app.run(host='0.0.0.0', port=8080, debug=True)
