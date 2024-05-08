#!/bin/bash
USERNAME_OLD=${1}
USERNAME_NEW=${2}

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
#Check if second argument is set
if [ -z "${2}" ]; then
    echo "ERROR: Please provide a new username as the second argument"
    exit 1
fi


# Create ldif file for user with echo command, multiline
echo "dn: uid=${USERNAME_OLD},cn=users,dc=nas-admin,dc=nota,dc=ai
changetype: modify
delete: cn
cn: ${USERNAME_OLD}
-
add: cn
cn: ${USERNAME_NEW}
-
dn: uid=${USERNAME_OLD},cn=users,dc=nas-admin,dc=nota,dc=ai
changetype: modify
delete: homeDirectory
homeDirectory: /home/${USERNAME_OLD}
-
add: homeDirectory
homeDirectory: /home/${USERNAME_NEW}
-
dn: uid=${USERNAME_OLD},cn=users,dc=nas-admin,dc=nota,dc=ai
changetype: modify
delete: sn
sn: ${USERNAME_OLD}
-
add: sn
sn: ${USERNAME_NEW}
-
dn: uid=${USERNAME_OLD},cn=users,dc=nas-admin,dc=nota,dc=ai
changetype: modify
delete: displayName
displayName: ${USERNAME_OLD}
-
add: displayName
displayName: ${USERNAME_NEW}
-
dn: uid=${USERNAME_OLD},cn=users,dc=nas-admin,dc=nota,dc=ai
changetype: moddn
newrdn: uid=${USERNAME_NEW}
deleteoldrdn: 1
newsuperior: cn=users,dc=nas-admin,dc=nota,dc=ai
-
" > /tmp/${1}.ldif

#echo "dn: uid=${USERNAME_OLD},cn=users,dc=nas-admin,dc=nota,dc=ai
#changetype: moddn
#newrdn: uid=${USERNAME_NEW}
#deleteoldrdn: 1
#newsuperior: cn=users,dc=nas-admin,dc=nota,dc=ai
#" > /tmp/${2}.ldif
# dn: uid=ubuntu_ldap,cn=users,dc=nas-admin,dc=nota,dc=ai
  #changetype: moddn
  #newrdn: uid=ubuntu_ldap_new
  #deleteoldrdn: 1
  #newsuperior: cn=users,dc=nas-admin,dc=nota,dc=ai
set -x
ldapmodify -v -D ${BIND_DN} -H ldap://nas-admin.nota.ai  -w ${BIND_PW} -f /tmp/${1}.ldif
#ldapmodify -v -D ${BIND_DN} -H ldap://nas-admin.nota.ai  -w ${BIND_PW} -f /tmp/${2}.ldif
set +x