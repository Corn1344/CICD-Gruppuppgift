FROM python

WORKDIR /test

COPY . .

RUN apt install Flask apscheduler validators requests

ENTRYPOINT flask run --host=0.0.0.0
