FROM python:3.7-slim

RUN useradd -rm -d /home/thanos -s /bin/bash -g root -G sudo -u 1000 thanos
RUN export DEBIAN_FRONTEND=noninteractive && \
apt-get -y update 

USER root
RUN addgroup thanos dialout

USER thanos

WORKDIR /usr/thanos/app

COPY . ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

ENV PATH=$PATH:/home/thanos/.local/bin

RUN export PYTHONPATH="${PYTHONPATH}:/usr/thanos/app/src"

CMD python3.7 run.py
