# import pandas as pd
import argparse
import csv
import io
import logging
import os.path
from datetime import datetime, timedelta, timezone
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3

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
arg_parser.add_argument("--filename", default="ec2-list-with-config.csv")
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
        end_date = target_time.replace(month=current_time.month, day=target_day, hour=0, minute=0, second=0,
                                       microsecond=0)
        if args.previous:
            end_date = target_time.replace(month=current_time.month, day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        end_date = target_time.replace(month=target_month, day=1, hour=0, minute=0, second=0, microsecond=0)

    for each_event in events:
        if each_event['EventName'] == 'StartInstances':
            if end_date < each_event['EventTime']:
                end_date = target_time.replace(month=current_time, day=1, hour=0, minute=0, second=0, microsecond=0)
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


def get_instance_type_info(instance_type):
    ec2_client = boto3.client('ec2', 'ap-northeast-2', aws_access_key_id=args.aws_access_key,
                              aws_secret_access_key=args.aws_secret_access_key)
    response = ec2_client.describe_instance_types(InstanceTypes=[instance_type])
    vcpus = response['InstanceTypes'][0]['VCpuInfo']['DefaultVCpus']
    mem_size = response['InstanceTypes'][0]['MemoryInfo']['SizeInMiB']
    return {"vcpus": vcpus, "mem_size": mem_size}


def main():
    ec2_client = boto3.resource('ec2', 'ap-northeast-2',
                                aws_access_key_id=args.aws_access_key, aws_secret_access_key=args.aws_secret_access_key)
    instance_ids = []
    for instance in ec2_client.instances.all():
        instance_state = instance.state['Name']
        instance_type = instance.instance_type
        instance_info = get_instance_type_info(instance_type)
        instance_volumes = instance.volumes.all()
        last_launch_time = instance.launch_time
        instance_name = get_instance_name(instance)
        for volume in instance_volumes:
            if volume.attachments[0]['State'] == 'attached':
                instance_ids.append(
                    {"id": str(instance.id), "state": instance_state, "name": instance_name,
                     "launch_time": last_launch_time,
                     "instance_type": instance_type, "memory": instance_info['mem_size'],
                     "cores": instance_info['vcpus'],
                     "volume_id": volume.id, "volume_size": volume.size})

    usage_info = []
    for i in instance_ids:
        usage_info.append(i)

    # Sort instances by last launch time
    output = io.StringIO()
    column_names = ['id', 'state', 'name', 'launch_time', 'instance_type', 'memory', 'cores', 'volume_id',
                    'volume_size']
    writer = csv.DictWriter(output, fieldnames=column_names)
    writer.writeheader()
    for usage in instance_ids:
        writer.writerow(
            {"id": usage['id'], "state": usage['state'], "name": usage['name'], "launch_time": usage['launch_time'],
             "instance_type": usage['instance_type'], "memory": usage['memory'], "cores": usage['cores'],
             "volume_id": usage['volume_id'], "volume_size": usage['volume_size']})
    # print(output.getvalue())
    filename = args.filename
    with open(filename, 'w') as csvfile:
        csvfile.write(output.getvalue())
    ses_client = boto3.client("ses", region_name="ap-northeast-2", aws_access_key_id=args.aws_access_key,
                              aws_secret_access_key=args.aws_secret_access_key)
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
