FROM jenkins/jenkins:2.350
USER root
RUN apt-get update
RUN apt-get install -y vim build-essential curl wget apt-transport-https \
    ca-certificates gnupg2 software-properties-common
#RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
#RUN apt-key fingerprint 0EBFCD88
#RUN add-apt-repository \
#       "deb [arch=amd64] https://download.docker.com/linux/debian \
#       $(lsb_release -cs) stable"
#RUN apt-get update && apt-get install -y docker-ce-cli
#ADD  ./tools /usr/local/tools
#RUN chmod +x /usr/local/tools/*
USER jenkins
#RUN jenkins-plugin-cli --plugins "blueocean:1.24.7 docker-workflow:1.26"
