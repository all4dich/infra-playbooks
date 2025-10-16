FROM ubuntu:24.04
LABEL authors="sunjoo"
LABEL description="Ansible Galaxy Environment Dockerfile"
RUN apt-get update && apt-get install -y procps vim build-essential curl wget git iputils-ping dnsutils net-tools
RUN apt-get install -y python3 python3-pip python3-venv
RUN pip3 install --break-system-packages ansible ansible-lint molecule[docker] yamllint testinfra
RUN mkdir -p /workspace
WORKDIR /workspace

ENTRYPOINT ["top", "-b"]