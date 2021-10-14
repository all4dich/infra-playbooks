ansible all -i common/all-servers.yaml -m copy -a "src=/Users/sunjoo/work/nota-github/modelsearch-infra-tools/monitoring-env/cAdvisor  dest=~/program"

ansible all -i common/all-servers.yaml -m shell -a "(cd ~/program/cAdvisor && docker compose up -d)"

ansible all -i common/all-servers.yaml -m shell -a "netstat -an|grep 49998" 

ansible all -i common/all-servers.yaml -m shell -a "rm -rfv ~/program/node*"

ansible all -i common/all-servers.yaml -m copy -a "src=/Users/sunjoo/work/nota-github/modelsearch-infra-tools/monitoring-env/node-exporter dest=~/program"

ansible all -i common/all-servers.yaml -m shell -a " pkill -f '.*node_exporter.*'"


ansible all -i common/all-servers.yaml -m shell -a "(cd ~/program/node-exporter && chmod +x node_exporter && sh run-exporter.sh)"

ansible all -i common/all-servers.yaml -m shell -a "(cd ~/program/node-exporter && chmod +x node_exporter && sh run-exporter.sh)"

ansible all -i common/all-servers.yaml -m shell -a "ps -ef|grep node_export"