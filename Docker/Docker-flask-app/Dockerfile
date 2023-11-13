FROM python

WORKDIR /test

COPY /var/jenkins_home/workspace/clone-gh-repo-jenkins/backend .

RUN apt install Flask apscheduler validators requests

ENTRYPOINT flask run --host=0.0.0.0
