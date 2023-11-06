# infra-playbooks
This repository keeps Ansible or other toolkits artifacts  to manage  Nota's development infra

## jenkins-env
### How to deploy 
Run `docker-compoe up -d` command on 'jenkins-env' directory

## ansible
### How to Use 
Move to 'ansible' directory and open README.md and follow its description

## GPU Server
### Get GPU Status with date and time range
1. Prepare SMTP User and Password for sending email
2. Run this command on your host
```shell
python3 python/src/main/get-gpu-usage.py --aws_access_key=xxxxxx --aws_secret_access_key=xxxxx --receiver=sunjoo.park@nota.ai 
```
```shell
python3 python/src/main/get-gpu-usage.py --help
usage: get-gpu-usage.py [-h] [--aws_access_key AWS_ACCESS_KEY]
                        [--aws_secret_access_key AWS_SECRET_ACCESS_KEY]
                        [--receiver RECEIVER] [--sender SENDER]
                        [--prometheus_url PROMETHEUS_URL] [--metric METRIC]
                        [--start_time START_TIME] [--end_time END_TIME]
                        [--step STEP] [--delete_temp_file]
                        [--smtp_host SMTP_HOST] [--smtp_port SMTP_PORT]

optional arguments:
  -h, --help            show this help message and exit
  --aws_access_key AWS_ACCESS_KEY
                        AWS Access Key or smpt username
  --aws_secret_access_key AWS_SECRET_ACCESS_KEY
                        AWS Secret Access Key or smpt password
  --receiver RECEIVER   Email address to get a result
  --sender SENDER       Email address to send a result
  --prometheus_url PROMETHEUS_URL
                        Prometheus URL
  --metric METRIC       Prometheus metric name
  --start_time START_TIME
                        Start time
  --end_time END_TIME   End time
  --step STEP           Step time for prometheus query
  --delete_temp_file    Delete temporary files
  --smtp_host SMTP_HOST
                        SMTP host
  --smtp_port SMTP_PORT
                        SMTP port
```
3. Check your email inbox and convert CSV file to worksheet files
4. Open worksheet files and check GPU usage

### Get GPU Status with monthly
1. Prepare SMTP User and Password for sending email
2. Run this command on your host
```shell
python3 python/src/main/get-gpu-usage-monthly.py --aws_access_key=xxxxxx --aws_secret_access_key=xxxxx --receiver=sunjoo.park@nota.ai 
```
```shell
python3 python/src/main/get-gpu-usage-monthly.py --help


usage: get-gpu-usage-monthly.py [-h] [--aws_access_key AWS_ACCESS_KEY] [--aws_secret_access_key AWS_SECRET_ACCESS_KEY] [--receiver RECEIVER] [--sender SENDER] [--prometheus_url PROMETHEUS_URL] [--metric METRIC] [--start_time START_TIME] [--end_time END_TIME] [--step STEP] [--delete_temp_file]
                                [--smtp_host SMTP_HOST] [--smtp_port SMTP_PORT] [--gpu-assigned-table GPU_ASSIGNED_TABLE] [--pivot-index PIVOT_INDEX] [--pivot-columns PIVOT_COLUMNS] [--pivot-values PIVOT_VALUES] [--pivot-aggfunc PIVOT_AGGFUNC]

optional arguments:
  -h, --help            show this help message and exit
  --aws_access_key AWS_ACCESS_KEY
                        AWS Access Key or smpt username
  --aws_secret_access_key AWS_SECRET_ACCESS_KEY
                        AWS Secret Access Key or smpt password
  --receiver RECEIVER   Email address to get a result
  --sender SENDER       Email address to send a result
  --prometheus_url PROMETHEUS_URL
                        Prometheus URL
  --metric METRIC       Prometheus metric name
  --start_time START_TIME
                        Start time
  --end_time END_TIME   End time
  --step STEP           Step time for prometheus query
  --delete_temp_file    Delete temporary files
  --smtp_host SMTP_HOST
                        SMTP host
  --smtp_port SMTP_PORT
                        SMTP port
  --gpu-assigned-table GPU_ASSIGNED_TABLE
                        GPU assigned table
  --pivot-index PIVOT_INDEX
  --pivot-columns PIVOT_COLUMNS
  --pivot-values PIVOT_VALUES
  --pivot-aggfunc PIVOT_AGGFUNC

```
3. Check your email inbox and convert CSV file to worksheet files
4. Open worksheet files and check GPU usage