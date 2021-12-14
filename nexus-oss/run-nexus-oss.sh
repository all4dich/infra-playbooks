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
export NEXUS_DATA="${1}"
if [ "${NEXUS_DATA}" = "" ]; then
  echo "ERROR: Please provide NEXUS_DATA directory path as the first argument for this script"
else
  echo "INFO: Nexus data directory = ${NEXUS_DATA}"
fi
if [ ! -d "${NEXUS_DATA}" ]; then
  sudo mkdir -p "${NEXUS_DATA}"
else
  echo "EXIST: ${NEXUS_DATA}"
fi
sudo chown -R 200:200 ${NEXUS_DATA}
docker-compose up -d
set +x