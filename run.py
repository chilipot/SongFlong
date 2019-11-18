from app import create_app
from rq import Worker


app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=False, threaded=True)