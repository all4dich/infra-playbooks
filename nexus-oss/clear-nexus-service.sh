#!/bin/bash
set -x
DOCKER_COMPOSE_TARGET="/usr/local/bin/docker-compose"
if ! command -v docker-compose; then
  sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" \
    -o ${DOCKER_COMPOSE_TARGET}
  sudo chmod +x ${DOCKER_COMPOSE_TARGET}
  sudo ln -s ${DOCKER_COMPOSE_TARGET} /usr/bin/docker-compose
else
  echo "INFO: $(command -v docker-compose)"
fi
export NEXUS_PERSISTENCE="/opt/nota/nexus-oss"
docker-compose down
sudo rm -rf ${NEXUS_PERSISTENCE}
set +x