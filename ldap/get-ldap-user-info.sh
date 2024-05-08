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


#ldapsearch -x -b dc=nas-admin,dc=nota,dc=ai  -D ${BIND_DN} -H ldap://nas-admin.nota.ai  -w ${BIND_PW} -s sub "uid=${1}"
# Get uidNumber and homeDirectory  and loginShell with ldapsearch
export uidNumber=`ldapsearch -x -b dc=nas-admin,dc=nota,dc=ai  -D ${BIND_DN} -H ldap://nas-admin.nota.ai  -w ${BIND_PW} -s sub "uid=${1}"|grep uidNumber|awk '{print $2}'`
export gidNumber=`ldapsearch -x -b dc=nas-admin,dc=nota,dc=ai  -D ${BIND_DN} -H ldap://nas-admin.nota.ai  -w ${BIND_PW} -s sub "uid=${1}"|grep gidNumber|awk '{print $2}'`
export homeDirectory=`ldapsearch -x -b dc=nas-admin,dc=nota,dc=ai  -D ${BIND_DN} -H ldap://nas-admin.nota.ai  -w ${BIND_PW} -s sub "uid=${1}"|grep homeDirectory|awk '{print $2}'`
export loginShell=`ldapsearch -x -b dc=nas-admin,dc=nota,dc=ai  -D ${BIND_DN} -H ldap://nas-admin.nota.ai  -w ${BIND_PW} -s sub "uid=${1}"|grep loginShell|awk '{print $2}'`
echo "uid: "${uidNumber}
echo "gid: "${gidNumber}
echo ${homeDirectory}
echo ${loginShell}

