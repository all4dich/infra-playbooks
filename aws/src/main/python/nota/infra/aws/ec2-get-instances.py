import boto3
import json
# import pandas as pd
import argparse
import logging
import os
from datetime import datetime, timedelta, timezone

from botocore.exceptions import ClientError

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

from email.mime.application import MIMEApplication

import urllib

import os.path
from multiprocessing import Pool
import io
import csv
import calendar

log_level: str = os.getenv("LOG_LEVEL", default="INFO")
log_console_format = "[%(levelname)s] %(asctime)s - %(name)s - %(message)s (in %(pathname)s:%(lineno)d)"
logging.basicConfig(format=log_console_format, datefmt="%m/%d/%Y %I:%M:%S %p %Z")
numeric_level = getattr(logging, log_level.upper(), None)
logging.getLogger().setLevel(numeric_level)

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("--aws_access_key")
arg_parser.add_argument("--aws_secret_access_key")
arg_parser.add_argument("--receiver")
arg_parser.add_argument("--sender", default="netspresso@nota.ai")
arg_parser.add_argument("--previous", action="store_true")
args = arg_parser.parse_args()

yesterday = datetime.today()


# Create a function to solve hanoi problem.

def get_events(instance_data):
    instance_id = instance_data['id']
    instance_state = instance_data['state']
    instance_name = instance_data['name']
    launch_time = instance_data['launch_time']
    cloudtrail = boto3.client('cloudtrail', 'ap-northeast-2', aws_access_key_id=args.aws_access_key,
                              aws_secret_access_key=args.aws_secret_access_key)
    current_time = datetime.now(timezone.utc)
    target_time = current_time
    target_month = target_time.month
    target_day = target_time.day

    if args.previous:
        first_day = target_time.replace(day=1)
        target_time = first_day - timedelta(days=1)
        target_month = target_time.month
        target_day = 1

    response = cloudtrail.lookup_events(
        LookupAttributes=[
            {
                'AttributeKey': 'ResourceName',
                'AttributeValue': instance_id
            }
        ],
        StartTime=target_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0),
        EndTime=current_time.replace(day=target_day, hour=0, minute=0, second=0, microsecond=0),
    )
    events_1 = filter(lambda x: x['EventName'] in ['StartInstances', 'StopInstances'], response['Events'])
    events = sorted(events_1, key=lambda x: x['EventTime'], reverse=True)
    total_duration = timedelta(0)

    if instance_state == "running":
        end_date = target_time.replace(month=current_time.month, day=target_day, hour=0, minute=0, second=0, microsecond=0)
        if args.previous:
            end_date = target_time.replace(month=current_time.month, day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        end_date = target_time.replace(month=target_month, day=1, hour=0, minute=0, second=0, microsecond=0)

    for each_event in events:
        if each_event['EventName'] == 'StartInstances':
            if end_date < each_event['EventTime']:
                end_date = target_time.replace(month=current_time.month, day=1, hour=0, minute=0, second=0, microsecond=0)
            total_duration = total_duration + (end_date - each_event['EventTime'])
            end_date = target_time.replace(month=target_month, day=1, hour=0, minute=0, second=0, microsecond=0)
        elif each_event['EventName'] == 'StopInstances':
            end_date = each_event['EventTime']

    total_duration = total_duration + (
            end_date - target_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0))

    a = {"id": instance_id, "state": instance_state, "name": instance_name,
         "total_duration": str(total_duration),
         "launch_time": launch_time, "events": events}
    return a


def get_instance_info(ec2_id):
    ec2_client = boto3.client('ec2', 'ap-northeast-2', aws_access_key_id=args.aws_access_key,
                              aws_secret_access_key=args.aws_secret_access_key)
    cloudtrail = boto3.client('cloudtrail', 'ap-northeast-2', aws_access_key_id=args.aws_access_key,
                              aws_secret_access_key=args.aws_secret_access_key)
    instance_info = ec2_client.describe_instances(InstanceIds=[
        ec2_id,
    ])

    instance_events = cloudtrail.lookup_events(
        LookupAttributes=[
            {
                'AttributeKey': 'ResourceName',
                'AttributeValue': ec2_id
            },

        ],
    )

    launch_time = instance_info['Reservations'][0]['Instances'][0]['LaunchTime']
    state = instance_info['Reservations'][0]['Instances'][0]['State']['Name']
    instance_name = "None"
    for tag in instance_info['Reservations'][0]['Instances'][0]['Tags']:
        if tag['Key'] == 'Name':
            instance_name = tag['Value']

    print(ec2_id, instance_name, launch_time, state, "\n")


def get_instance_name(instance):
    instance_name = ""
    for each_tag in instance.tags:
        if each_tag['Key'] == 'Name':
            instance_name = each_tag['Value']
            break
    return str(instance_name)


def main():
    ec2_client = boto3.resource('ec2', 'ap-northeast-2',
                                aws_access_key_id=args.aws_access_key, aws_secret_access_key=args.aws_secret_access_key)
    instance_ids = []
    for instance in ec2_client.instances.all():
        instance_state = instance.state['Name']
        last_launch_time = instance.launch_time
        instance_name = get_instance_name(instance)
        instance_ids.append(
            {"id": str(instance.id), "state": instance_state, "name": instance_name, "launch_time": last_launch_time})

    usage_info = []
    for i in instance_ids:
        usage_info.append(get_events(i))

    # Sort instances by last launch time
    sorted_instances = sorted(usage_info, key=lambda x: x['launch_time'], reverse=True)
    print(json.dumps(sorted_instances, default=str, ensure_ascii=False))
    output = io.StringIO()
    column_names = ['name', 'id', 'state', 'total_duration', 'launch_time']
    writer = csv.DictWriter(output, fieldnames=column_names)
    writer.writeheader()
    for usage in sorted_instances:
        writer.writerow({'name': usage['name'], 'id': usage['id'], 'state': usage['state'],
                         'total_duration': usage['total_duration'], 'launch_time': usage['launch_time']})
    #print(output.getvalue())
    filename = "output.csv"
    with open(filename , 'w') as csvfile:
        csvfile.write(output.getvalue())
    ses_client = boto3.client("ses", region_name="ap-northeast-2", aws_access_key_id=args.aws_access_key, aws_secret_access_key=args.aws_secret_access_key)
    CHARSET = "UTF-8"
    msg = MIMEMultipart()
    msg["Subject"] = "AWS EC2 Usage"
    msg["From"] = "administrator@nota.ai"
    msg["To"] = "sunjoo.park@nota.ai"

    # Set message body
    body = MIMEText("Nota AWS EC2 Usage", "plain")
    msg.attach(body)

    with open(filename, "rb") as attachment:
        part = MIMEApplication(attachment.read())
        part.add_header("Content-Disposition",
                        "attachment",
                        filename=filename)
    msg.attach(part)

    # Convert message to string and send
    ses_client = boto3.client("ses", region_name="ap-northeast-2")
    response = ses_client.send_raw_email(
        Source="administrator@nota.ai",
        Destinations=["sunjoo.park@nota.ai"],
        RawMessage={"Data": msg.as_string()}
    )
    print(response)



if __name__ == "__main__":
    main()
