FROM python:3.7-alpine AS base-image

LABEL Author="Daniel Guddemi danguddemi@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /songflong/requirements.txt

RUN apk update && \
    apk add --no-cache --virtual .build-deps build-base linux-headers git g++ gcc libc-dev libxslt-dev && \
    apk add --no-cache libxslt jpeg-dev zlib-dev && \
    pip wheel --wheel-dir=/root/wheels -r /songflong/requirements.txt &&\
    apk del .build-deps

FROM python:3.7-alpine

COPY --from=base-image /root/wheels /root/wheels

COPY ./requirements.txt /songflong/requirements.txt

WORKDIR /songflong

RUN apk add --no-cache libxslt ffmpeg jpeg-dev zlib-dev git && \
    pip install \
      --no-index \
      --find-links=/root/wheels \
      -r requirements.txt


COPY ./run.py /songflong/run.py
COPY ./worker.py /songflong/worker.py
COPY ./app /songflong/app

ENTRYPOINT [ "python" ]
CMD [ "run.py" ]