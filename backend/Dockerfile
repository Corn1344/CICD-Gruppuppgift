FROM python

WORKDIR /test

COPY . .

RUN apt update -y

RUN apt install python3-flask python3-apscheduler python3-validators python3-requests -y

ENTRYPOINT flask run --host=0.0.0.0
