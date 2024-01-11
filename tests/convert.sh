#!/bin/bash
# check if first argument is set
if [ -z "${1}" ]; then
    echo "ERROR: Please provide a username as the first argument"
    exit 1
else
    export username=${1}
fi
# Check if second argument is set
if [ -z "${2}" ]; then
    echo "ERROR: Please provide a hostname as the second argument"
    exit 1
else
    export hostname=${2}
fi
# Check if third argument is set
if [ -z "${3}" ]; then
    echo "ERROR: Use ${username} as new_username "
    export new_username=${username}
else
    export new_username=${3}
fi
ansible-playbook -i inventory/all-servers.yaml   -e target_user=${username} -e target_host=${hostname} -e new_username=${new_username} playbooks/ldap-convert-local-to-ldap-account.yaml