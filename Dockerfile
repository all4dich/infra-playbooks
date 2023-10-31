FROM python:3.9.16
LABEL authors="sunjoo.park"
RUN apt-get update -y
RUN apt-get install -y vim build-essential curl wget apt-transport-https  ca-certificates gnupg2 software-properties-common git
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
ENTRYPOINT ["/bin/bash"]