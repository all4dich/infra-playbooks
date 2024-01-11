#!/bin/bash
TARGETS=(
all,intern
)

#echo ${TARGETS}
for a in "${TARGETS[@]}"
do
  # Split a into an array
  IFS=',' read -r -a array <<< "$a"
  hostname=${array[0]}
  username=${array[1]}
  #ansible-playbook -i inventory/all-servers.yaml playbooks/check-user-directory-size.yaml -e target_user=${username} -e target_host=${hostname}
  ansible-playbook -i inventory/all-servers.yaml playbooks/delete-user-on-server.yaml -e target_user=${username} -e target_host=${hostname}
done
