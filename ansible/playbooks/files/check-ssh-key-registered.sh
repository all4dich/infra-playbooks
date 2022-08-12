#!/bin/bash

# Get a list of registered users
USERS=$(cat /etc/passwd|awk -F: '{print $1","$3}'|grep -E '\,[0-9]{4}$')
HOSTNAME=$(hostname)
for a in ${USERS}
do
    IFS=',' read -r -a USER_INFO <<< "$a"
    USER_NAME=${USER_INFO[0]}
    USER_UID=${USER_INFO[1]}
    # Check if user has never logged onto a machine
    if [ "${USER_NAME}" = "docker" ] || [ "${USER_NAME}" = "mysql" ]; then
        USER_ACCOUNT=0
    else
        USER_ACCOUNT=1
    fi
    if [ "${USER_ACCOUNT}" = 1 ]; then
      if [ -f `eval echo ~${USER_NAME}/.ssh/authorized_keys` ] && [ -f `eval echo ~${USER_NAME}/.ssh/id_rsa.pub` ]; then
        KEY_VALUE=`cat ~${USER_NAME}/.ssh/id_rsa.pub`
        CHECK_COUNT=`cat ~${USER_NAME}/.ssh/authorized_keys|grep ${KEY_VALUE}`
        if [ "${CHECK_COUNT}" = "1" ]; then
          echo ${HOSTNAME},${USER_NAME},"registered"
        else
          echo ${HOSTNAME},${USER_NAME},"registered"
        fi
      else
        echo ${HOSTNAME},${USER_NAME},"not registered"
      fi
    fi
done