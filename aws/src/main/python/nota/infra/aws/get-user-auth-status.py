import boto3
import pandas as pd
import argparse
import logging
import os

log_level: str = os.getenv("LOG_LEVEL", default="INFO")
log_console_format = "[%(levelname)s] %(asctime)s - %(name)s - %(message)s (in %(pathname)s:%(lineno)d)"
logging.basicConfig(format=log_console_format, datefmt="%m/%d/%Y %I:%M:%S %p %Z")
numeric_level = getattr(logging, log_level.upper(), None)
logging.getLogger().setLevel(numeric_level)

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("--csv")
args = arg_parser.parse_args()

iam_client = boto3.client('iam')


def get_access_key_last_used(UserName):
    user_keys = iam_client.list_access_keys(UserName=UserName)
    last_used_date = None
    last_used_key = None
    for each_key in user_keys['AccessKeyMetadata']:
        access_key_id = each_key['AccessKeyId']
        last_accessed_info = iam_client.get_access_key_last_used(AccessKeyId=access_key_id)
        if 'LastUsedDate' in last_accessed_info['AccessKeyLastUsed']:
            used_data = last_accessed_info['AccessKeyLastUsed']['LastUsedDate']
            if last_used_date is None or last_used_date < used_data:
                last_used_date = used_data
                last_used_key = access_key_id
    return last_used_key, last_used_date


def get_user_access_list():
    all_users = iam_client.list_users()['Users']
    df_raw = {"user_name": [],
              "password_last_used": [],
              "last_key_used": [],
              "last_key_date": [],
              }
    i = 0
    for each_user in all_users:
        user_name = each_user['UserName']
        user_id = each_user['UserId']
        password_last_used = None
        if 'PasswordLastUsed' in each_user:
            password_last_used = each_user['PasswordLastUsed']
        last_key_used, last_key_date = get_access_key_last_used(user_name)
        df_raw["user_name"].append(user_name)
        df_raw["password_last_used"].append(password_last_used)
        df_raw["last_key_used"].append(last_key_used)
        df_raw["last_key_date"].append(last_key_date)
    if args.csv:
        logging.info(f"Output will be on {args.csv}")
        pd.DataFrame(df_raw).to_csv(args.csv, index=False)
    else:
        print(pd.DataFrame(df_raw).to_csv(index=False))
    logging.info("Done")


if __name__ == "__main__":
    get_user_access_list()
