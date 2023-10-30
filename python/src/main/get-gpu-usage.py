import requests
from datetime import datetime, timezone, timedelta
import json
import csv
import os
import logging
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import boto3
import zipfile
import tempfile
import smtplib
import pandas as pd

datetime_format = "%Y-%m-%d %H:%M:%S %Z"
log_level: str = os.getenv("LOG_LEVEL", default="INFO")
log_console_format = "[%(levelname)s] %(asctime)s - %(name)s - %(message)s (in %(pathname)s:%(lineno)d)"
logging.basicConfig(format=log_console_format, datefmt=datetime_format)
numeric_level = getattr(logging, log_level.upper(), None)
logging.getLogger().setLevel(numeric_level)

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("--aws_access_key", help="AWS Access Key or smpt username")
arg_parser.add_argument("--aws_secret_access_key", help="AWS Secret Access Key or smpt password")
arg_parser.add_argument("--receiver", help="Email address to get a result")
arg_parser.add_argument("--sender", default="administrator@nota.ai", help="Email address to send a result")
arg_parser.add_argument("--prometheus_url", default="https://infra.nota.ai/prometheus/", help="Prometheus URL")
arg_parser.add_argument("--metric", default="DCGM_FI_DEV_GPU_UTIL", help="Prometheus metric name" )
arg_parser.add_argument("--start_time",
                        default=(datetime.now(timezone.utc) - timedelta(weeks=2)).strftime(datetime_format), help="Start time")
arg_parser.add_argument("--end_time", default=(datetime.now(timezone.utc)).strftime(datetime_format), help="End time")
arg_parser.add_argument("--step", default="5m", help="Step time for prometheus query")
arg_parser.add_argument("--delete_temp_file", action="store_true", default=True, help="Delete temporary files")
arg_parser.add_argument("--smtp_host", default="email-smtp.ap-northeast-2.amazonaws.com", help="SMTP host")
arg_parser.add_argument("--smtp_port", default=587, type=int, help="SMTP port")
arg_parser.add_argument("--gpu-assigned-table", help="GPU assigned table")
arg_parser.add_argument("--pivot-index", default="week,team,part,person")
arg_parser.add_argument("--pivot-columns", default="hostname")
arg_parser.add_argument("--pivot-values", default="is_used")
arg_parser.add_argument("--pivot-aggfunc", default="sum")


args = arg_parser.parse_args()
server_url = args.prometheus_url
metric_name = args.metric

gpu_assign_list_new = []
gpu_assign_list_new_key = ['gpu_id', 'hostname', 'team', 'part', 'person', 'gpu_key']

def get_usage_data(start_date, end_date, step="5m"):
    start = datetime.strptime(start_date, datetime_format)
    end = datetime.strptime(end_date, datetime_format)
    query_url = server_url + "api/v1/query_range?query=" + metric_name + "&step=" + step + "&start=" + str(
        start.timestamp()) + "&end=" + str(end.timestamp())
    r = requests.get(url=query_url, verify=False)
    response_data = json.loads(r.text)
    return response_data


def write_to_file(data):
    column_names = ['hostname', 'gpu model', 'gpu id', 'gpu_uuid', 'check time', 'year', 'month', 'day', 'week', 'utilization',
                    'is_used', 'team', 'part', 'person']
    gpu_assign_dict = {}
    gpu_assign_list = {}
    if args.gpu_assigned_table:
        with open(args.gpu_assigned_table, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            gpu_assign_list = list(reader)
        # Convert the list to a dictionary
        for row in gpu_assign_list:
            gpu_key = row['Host'].lower() + '-' + row['GPU_id']
            gpu_assign_dict[row['Host'].lower() + '-' + row['GPU_id']] = row
            row['gpu_key'] = gpu_key
            gpu_assign_list_new.append([row['GPU_id'], row['Host'], row['Team'], row['Part'], row['Person'], row['gpu_key']])
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as output:
        csv_writer = csv.DictWriter(output, fieldnames=column_names)
        csv_writer.writeheader()
        for a in data['data']['result']:
            try:
                hostname = a['metric']['Hostname']
                model_name = a['metric']['modelName']
                gpu_id = a['metric']['gpu']
                gpu_uuid = a['metric']['UUID']
                values = a['values']
                team = ""
                part = ""
                person = ""
                if args.gpu_assigned_table:
                    if hostname.lower() + '-' + gpu_id in gpu_assign_dict:
                        team = gpu_assign_dict[hostname.lower() + '-' + gpu_id]['Team']
                        part = gpu_assign_dict[hostname.lower() + '-' + gpu_id]['Part']
                        person = gpu_assign_dict[hostname.lower() + '-' + gpu_id]['Person']

                for i in values:
                    check_time = datetime.fromtimestamp(i[0])
                    metric_value = int(i[1])
                    is_used = 1 if metric_value > 0 else 0
                    csv_writer.writerow({
                        'hostname': hostname, 'gpu model': model_name, 'gpu id': gpu_id, 'gpu_uuid': gpu_uuid, 'check time': check_time,
                        'year': check_time.year, 'month': check_time.month, 'day': check_time.day,
                        'week': check_time.strftime("%V"),
                        'utilization': metric_value, 'is_used': is_used,
                        'team': team, 'part': part, 'person': person
                    })
            except KeyError as e:
                logging.error(e)
                logging.error(a)
                exit(1)
        return output.name


if __name__ == "__main__":
    metric_data = get_usage_data(args.start_time, args.end_time, args.step)
    if metric_data['status'] == "error":
        logging.error("Can't get metric data from Prometheus.")
        logging.error(str(metric_data))
        exit(1)
    file_name = write_to_file(metric_data)
    logging.error("output file = " + file_name)
    file_name_zip = tempfile.TemporaryDirectory().name + str(args.end_time) + ".zip"
    logging.error("zip file = " + file_name_zip)

    with zipfile.ZipFile(file_name_zip, 'w', zipfile.ZIP_DEFLATED) as zip_writer:
        zip_writer.write(file_name, arcname=os.path.basename(args.end_time) + ".csv")

    # Convert csv file to pandas dataframe
    df = pd.read_csv(file_name)
    # Create pivot table
    target_index = args.pivot_index.split(",") if args.pivot_index else None
    target_columns = args.pivot_columns.split(",") if args.pivot_columns else None
    target_values = args.pivot_values.split(",") if args.pivot_values else None
    pivot = df.pivot_table(index=target_index, columns=target_columns, values=target_values, aggfunc=args.pivot_aggfunc)
    logging.info("Usage Pivot Table")
    logging.info(pivot)
    start = datetime.strptime(args.start_time, datetime_format)
    end = datetime.strptime(args.end_time, datetime_format)
    #slot_number = int((end - start).total_seconds() / 300)
    slot_number = (timedelta(weeks=1).total_seconds()/ 300)
    #pivot_index_count = df.pivot_table(index=target_index, columns=target_columns, values=target_values, aggfunc=lambda x: int(len(x.unique()) * slot_number))
    df_count = pd.DataFrame(gpu_assign_list_new, columns=gpu_assign_list_new_key)
    pivot_index_count = df_count.pivot_table(index=['team', 'part', 'person'], columns="hostname", values="gpu_key", aggfunc=lambda x: int(len(x.unique())) * slot_number)

    # Write pivot table to excel file
    temp_dir = tempfile.TemporaryDirectory()
    os.system("mkdir -p " + temp_dir.name)
    temp_file_path = os.path.join(temp_dir.name, args.end_time + "-pivot-table.xlsx")
    temp_pivot_count_file_path = os.path.join(temp_dir.name, args.end_time + "-pivot-count.xlsx")
    logging.info("Write a pivot table to " + temp_file_path)
    pivot.to_excel(temp_file_path)
    pivot_index_count.to_excel(temp_pivot_count_file_path)

    CHARSET = "UTF-8"
    msg = MIMEMultipart()
    msg["Subject"] = "GPU Usage"
    msg["From"] = args.sender
    msg["To"] = args.receiver

    # Set message body
    body = MIMEText("GPU Usage", "plain")
    msg.attach(body)

    with open(file_name_zip, "rb") as attachment:
        part = MIMEApplication(attachment.read())
        part.add_header("Content-Disposition",
                        "attachment",
                        filename=args.end_time + ".zip")
        msg.attach(part)

    with open(temp_file_path, "rb") as attachment2:
        part2 = MIMEApplication(attachment2.read())
        part2.add_header("Content-Disposition",
                        "attachment",
                        filename=args.end_time + "-pivot-table.xlsx")
        msg.attach(part2)

    with open(temp_pivot_count_file_path, "rb") as attachment3:
        part3 = MIMEApplication(attachment3.read())
        part3.add_header("Content-Disposition",
                        "attachment",
                        filename=args.end_time + "-pivot-count.xlsx")
        msg.attach(part3)

    # Send email to sender by smtplib
    try:
        logging.info("Send email to " + args.receiver + " by smtplib")
        smtp_client = smtplib.SMTP(args.smtp_host, args.smtp_port)
        smtp_client.starttls()
        smtp_client.login(args.aws_access_key, args.aws_secret_access_key)
        smtp_client.sendmail(args.sender, args.receiver, msg.as_string())
        smtp_client.quit()
    except Exception as e:
        logging.error("Can't send email to " + args.receiver + " by smtplib")
        logging.error(e)
    # delete temp file
    if args.delete_temp_file:
        logging.info("Delete temporary files")
        os.remove(file_name)
        os.remove(file_name_zip)
    logging.info("Assigned Datal")
    logging.info(pivot_index_count)
    logging.info("Done")
