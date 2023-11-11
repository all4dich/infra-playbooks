#!/bin/bash
set -x
# Check if aws command exists
if ! [ -x "$(command -v aws)" ]; then
  echo 'Error: aws command is not installed.' >&2
  exit 1
fi
# Check if 'aws iam get-user' command returns a valid user
if ! aws iam get-user > /dev/null 2>&1; then
  echo 'Error: aws command is not configured properly. Please check your AWS credentials and configurtion' >&2
  exit 1
fi
# Check if a script file get 2 arguments.
if [ $# -ne 3 ]; then
  echo "Error: Invalid number of arguments. Please specify target directory, database host and database port." >&2
  exit 1
fi
BACKUP_IDX=`LC_ALL=C date +%Y_%m_%d-%H:%m:%S`
TARGET_DIR=${1}
DATABASE_HOST=${2}
DATABASE_PORT=${3}
# Check if DATABASE_USER and DATABASE_PASSWORD are set
if [ -z ${DATABASE_USER} ] || [ -z ${DATABASE_PASSWORD} ]; then
  echo "Error: DATABASE_USER and DATABASE_PASSWORD must be set." >&2
  exit 1
fi
RESULT_FILE=${TARGET_DIR}/dump-${BACKUP_IDX}.sql
# check if USE_MYSQL is set or not
if [ -z ${USE_MYSQL} ]; then
  echo "Info: Dump with mariadb-dump command."
  mariadb-dump -u ${DATABASE_USER} -p${DATABASE_PASSWORD} -h${DATABASE_HOST} --port=${DATABASE_PORT} --all-databases --result-file=${RESULT_FILE}
else
  if [ ${USE_MYSQL} = "true" ]; then
    echo "Info: Dump with mysqldump command."
    mysqldump -u ${DATABASE_USER} -p${DATABASE_PASSWORD} -h${DATABASE_HOST} --port=${DATABASE_PORT} --all-databases --result-file=${RESULT_FILE} --single-transaction
  fi
fi
echo "Info: Upload ${RESULT_FILE} to S3."
aws s3 cp ${RESULT_FILE} s3://infra-backup-archives/database/${DATABASE_HOST}-${DATABASE_PORT}/
set +x