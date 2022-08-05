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
        CHECK_LOGIN=0
    else
        CHECK_LOGIN=`lastlog -u ${USER_NAME}|grep Never\ logged|wc -l`
    fi
    if [ "${CHECK_LOGIN}" = 1 ]; then
        HOME_SIZE=`bash -c "du -sh ~${USER_NAME}"|tr '\t' ','`
        echo ${HOSTNAME},${USER_NAME},${USER_UID},${HOME_SIZE}
    fi    
done