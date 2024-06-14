#!/bin/bash

# Check if BIND_DN and BIND_PW are set
if [ -z "${BIND_DN}" ] || [ -z "${BIND_PW}" ]; then
    echo "ERROR: BIND_DN or BIND_PW is not set"
    exit 1
fi

# Check if ${1} is set
if [ -z "${1}" ]; then
    echo "ERROR: Please provide a username as the first argument"
    exit 1
fi

# Check if second argument is set
if [ -z "${2}" ]; then
    echo "INFO: Use default 123456"
    newPassword="/bin/bash"
else
    newPassword="${2}"
fi


# Create ldif file for user with echo command, multiline
echo "dn: uid=${1},cn=users,dc=nas-admin,dc=nota,dc=ai
changetype: modify
replace: userPassword
userPassword: ${newPassword}
" > /tmp/${1}.ldif

set -x
ldapmodify -v -D ${BIND_DN} -H ldap://nas-admin.nota.ai  -w ${BIND_PW} -f /tmp/${1}.ldif
set +x