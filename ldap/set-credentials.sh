#!/bin/bash
export DOMAIN_NAME="nas-admin"
export DOMAIN="nota.ai"
export LDAP_HOST="nas.nota.ai"
export LDAP_SERVER="ldap://nas-admin.nota.ai"
export ROOT_DN="dc=nas-admin,dc=nota,dc=ai"
export BASE_DN="cn=users,dc=nas-admin,dc=nota,dc=ai"
export USER_BASE="cn=users,dc=nas-admin,dc=nota,dc=ai"
export GROUP_BASE="cn=groups,dc=nas-admin,dc=nota,dc=ai"

export user="admin"
export pass="wecgyv-dIjrov-tufxo7"

export BIND_DN="uid=${user},${BASE_DN}"
export BIND_PW=${pass}