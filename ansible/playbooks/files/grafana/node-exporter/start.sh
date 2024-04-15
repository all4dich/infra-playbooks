#!/bin/bash
# Download Node Exporter from https://prometheus.io/download/#node_exporter
#TARGET_DIR=`dirname $0`
FULL_PATH=`realpath $0`
TARGET_DIR=`dirname $FULL_PATH`
PORT=49997
cd $TARGET_DIR
archi=`uname -m`
if [ "$archi" == "x86_64" ]; then
    archi="amd64"
elif [ "$archi" == "aarch64" ]; then
    archi="arm64"
else
    echo "Unsupported architecture: $archi"
    exit 1
fi
if [ ! -f ./node_exporter ]; then
    wget  https://github.com/prometheus/node_exporter/releases/download/v1.7.0/node_exporter-1.7.0.linux-${archi}.tar.gz
    tar --strip-components=1 -xvzf node_exporter-1.7.0.linux-${archi}.tar.gz
fi
./node_exporter --web.listen-address=:${PORT}