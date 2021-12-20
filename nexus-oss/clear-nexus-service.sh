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
export NEXUS_DATA=${1}
if [ ! -d "${NEXUS_DATA}" ]; then
  echo "ERROR: ${NEXUS_DATA} doesn't exist "
  exit 1
fi
docker-compose down
sudo rm -rf ${NEXUS_DATA}
set +x