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
    CHECK_LOGIN=`LC_ALL=C lastlog -u ${USER_NAME}|tail -n 1`
    CONN_INFO="Never Logged"
    if [[ "${CHECK_LOGIN}" =~ [0-9]$ ]]; then
        CONN_INFO=`echo $CHECK_LOGIN|sed "s/${USER_NAME} //g"`
    fi
    echo ${HOSTNAME},${USER_NAME},${CONN_INFO}
done
