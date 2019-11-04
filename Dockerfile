FROM python:3.7-slim-buster

LABEL Author="Daniel Guddemi danguddemi@gmail.com"

RUN apt-get update -y &&\
    apt-get install -y git g++ gcc libxslt-dev libc-dev ffmpeg

COPY ./requirements.txt /songflong/requirements.txt

WORKDIR /songflong

RUN pip install -r requirements.txt

COPY ./run.py /songflong/run.py
COPY ./worker.py /songflong/worker.py
COPY ./app /songflong/app

ENTRYPOINT [ "python" ]
CMD [ "run.py" ]