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
    #CONN_INFO=`echo $CHECK_LOGIN|sed "s/${USER_NAME} //g"`
    HOME_DIR=` eval echo ~${USER_NAME}`
    chmod 700 ${HOME_DIR}
    HOME_PERMISSION=`ls -ld ${HOME_DIR}|awk '{print $1}'`
    echo ${HOSTNAME},${USER_NAME},${HOME_PERMISSION}
done
