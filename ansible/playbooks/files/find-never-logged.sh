#!/bin/bash

# Get a list of registered users
USERS=$(cat /etc/passwd|awk -F: '{print $1","$3}'|grep -E '\,[0-9]{4}$')
HOSTNAME=$(hostname)
for a in ${USERS}
do
    echo $HOSTNAME,$a
done