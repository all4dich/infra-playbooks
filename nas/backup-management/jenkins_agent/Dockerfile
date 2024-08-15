FROM ubuntu:22.04
LABEL authors="sunjoo.park<sunjoo.park@nota.ai>"
ENV TZ=UTC
ENV DEBIAN_FRONTEND=noninteractive
# Update package lists and install tzdata
RUN apt-get update && apt-get install -y tzdata && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && apt-get install -y rsync vim openjdk-17-jdk tmux python3-dev python3-pip curl unzip sudo build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
WORKDIR /tmt
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install
RUN useradd -u 1000115 -d /home/group.infra_team -m -s /bin/bash group.infra_team
