import argparse
import json
import logging
from nexus.account import NexusConnector
# Get username and password from arguments
parser = argparse.ArgumentParser()
parser.add_argument("--username", required=True)
parser.add_argument("--password", required=True)
parser.add_argument("--url", required=True)
parser.add_argument("--target_user", required=True)
args = parser.parse_args()
nexus_username = args.username
nexus_password = args.password
target_user = args.target_user
nexus_url = args.url


def helloworld():
    print("Hello, world")

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    nexus_connector = NexusConnector(account=nexus_username, password=nexus_password, url=nexus_url)
    role_name = "nota-people-" + target_user
    privileges = [
        "nx-repository-view-pypi-pypi-server-add",
        "nx-repository-view-pypi-pypi-server-browse",
        "nx-repository-view-pypi-pypi-server-edit",
        "nx-repository-view-pypi-pypi-server-read",
        "nx-repository-admin-pypi-pypi-server-browse",
        "nx-repository-admin-pypi-pypi-server-edit",
        "nx-repository-admin-pypi-pypi-server-read"
    ]
    nexus_connector.add_privileges_to_roles([role_name], privileges)
    r = nexus_connector.get_role_info(role_name)
    print("## Role info: ##")
    print(json.dumps(r, indent=2))
