#!/bin/bash
set -x
export DCGM_EXPORTER_LISTEN=":30001"
export DCGM_EXPORTER_INTERVAL="5000"
#export DCGM_EXPORTER_VERSION=2.1.4-2.3.1
export DCGM_EXPORTER_VERSION=2.2.9-2.5.0-ubi8
export DCGM_EXPORTER_COLLECTORS="/etc/dcgm-exporter/default-counters.csv"

docker run -d --rm \
--gpus all \
--net host \
--cap-add SYS_ADMIN \
-e DCGM_EXPORTER_LISTEN="${DCGM_EXPORTER_LISTEN}" \
-e DCGM_EXPORTER_INTERVAL="${DCGM_EXPORTER_INTERVAL}" \
-e DCGM_EXPORTER_COLLECTORS="${DCGM_EXPORTER_COLLECTORS}" \
-v $(pwd)/exporters:/etc/dcgm-exporter \
--name dcgm-exporter \
nvcr.io/nvidia/k8s/dcgm-exporter:${DCGM_EXPORTER_VERSION} 
set +x
