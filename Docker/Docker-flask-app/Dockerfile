FROM jenkins/jenkins

WORKDIR /test

COPY ../../backend .

RUN pip install Flask apscheduler validators requests

ENTRYPOINT flask run --host=0.0.0.0
