#!/bin/bash
#export AWS_SECRET_ACCESS_KEY=${INFRA_AWS_SECRET_ACCESS_KEY}
#export AWS_ACCESS_KEY_ID=${INFRA_AWS_ACCESS_KEY_ID}


DATABASE_USER=${DB_ADMIN_USERNAME_12} DATABASE_PASSWORD=${DB_ADMIN_PASSWORD_12} ./database/scripts/backup-to-s3.sh /tmp 10.169.10.12 3306
DATABASE_USER=${DB_ADMIN_USERNAME_12_43306} DATABASE_PASSWORD=${DB_ADMIN_PASSWORD_12_43306}      ./database/scripts/backup-to-s3.sh /tmp 10.169.10.12 43306
DATABASE_USER=${DB_ADMIN_USERNAME_14} DATABASE_PASSWORD=${DB_ADMIN_PASSWORD_14} ./database/scripts/backup-to-s3.sh /tmp 10.169.10.14 3306
DATABASE_USER=${DB_ADMIN_USERNAME_15} DATABASE_PASSWORD=${DB_ADMIN_PASSWORD_15} ./database/scripts/backup-to-s3.sh /tmp 10.169.10.15 13306
DATABASE_USER=${DB_ADMIN_USERNAME_NP_PROD} DATABASE_PASSWORD=${DB_ADMIN_PASSWORD_NP_PROD} ./database/scripts/backup-to-s3.sh /tmp netspresso-searcher-db.cmaie8phm9pn.ap-northeast-2.rds.amazonaws.com  3306
DATABASE_USER=${DB_ADMIN_NP_LOGIN_PROD_USERNAME} DATABASE_PASSWORD=${DB_ADMIN_NP_LOGIN_PROD_PASSWORD} ./database/scripts/backup-to-s3.sh /tmp netspresso-loginserver.cmaie8phm9pn.ap-northeast-2.rds.amazonaws.com 3306
USE_MYSQL=true DATABASE_USER=${DB_ADMIN_USERNAME_NP_STAGING} DATABASE_PASSWORD=${DB_ADMIN_PASSWORD_NP_STAGING} ./database/scripts/backup-to-s3.sh /tmp netspresso-modelsearch-staging.cmaie8phm9pn.ap-northeast-2.rds.amazonaws.com 3306
find /tmp -maxdepth 1 -type f -name "*sql" -user $(id -u) -exec rm -rfv {} \;