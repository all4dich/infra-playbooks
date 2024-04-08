import requests
import argparse
import os
import logging
import json

logging.getLogger().setLevel(logging.INFO)

# Get username and password from arguments
parser = argparse.ArgumentParser()
parser.add_argument("--username", required=True)
parser.add_argument("--password", required=True)
parser.add_argument("--url", required=True)
parser.add_argument("--target_group")
parser.add_argument("--target_user")
args = parser.parse_args()
nexus_username = args.username
nexus_password = args.password
nexus_url = args.url


def get_content_selectors():
    url = f"{nexus_url}/service/rest/v1/security/content-selectors"
    r = requests.get(url, auth=(nexus_username, nexus_password))
    print(r.text)


# get privilege from nexus repository
def get_privileges():
    url = f"{nexus_url}/service/rest/v1/security/privileges"
    r = requests.get(url, auth=(nexus_username, nexus_password))
    logging.info(f"Status code for getting privileges: {r.status_code}")
    print(r.text)


def create_content_selector_for_docker_group(target_group_name):
    url = f"{nexus_url}/service/rest/v1/security/content-selectors"
    cs_name = f"docker-nota-group-{target_group_name}"
    cs_expression = f"format == \"docker\" and path =^ \"/v2/nota/group/{target_group_name}/\""
    data = {
        "name": cs_name,
        "description": cs_name,
        "expression": cs_expression,
        "enabled": True
    }
    r = requests.post(url, json=data, auth=(nexus_username, nexus_password))
    logging.info(f"Status code for creating content selector for {target_group_name}: {r.status_code}")
    if r.status_code in [200, 201, 204]:
        logging.info(f"Successfully created content selector for {target_group_name}")
        return cs_name
    else:
        logging.error(r.text)
        return None


# Create privilege for the user
def create_privilege_for_docker_group(target_user_name):
    url = f"{nexus_url}/service/rest/v1/security/privileges/repository-content-selector"
    privilege_name = f"docker-nota-group-{target_user_name}"
    data = {
        "name": privilege_name,
        "description": privilege_name,
        "actions": ["ALL"],
        "format": "docker",
        "repository": "*",
        "contentSelector": privilege_name
    }
    r = requests.post(url, json=data, auth=(nexus_username, nexus_password))
    logging.info(f"Status code for creating privilege for {target_user_name}: {r.status_code}")
    if r.status_code in [200, 201, 204]:
        logging.info(f"Successfully created privilege for {target_user_name}")
        return privilege_name
    else:
        logging.error(r.text)
        return None


# Register account on nexus repository
def register_group(target_groupname, target_username="sunjoo.park"):
    cs_name = create_content_selector_for_docker_group(target_groupname)
    if cs_name is None:
        logging.error(f"Failed to create content selector for {target_groupname}")
        return
    logging.info(f"Successfully created content selector for {target_groupname}")
    privilage_name = create_privilege_for_docker_group(target_groupname)
    if privilage_name is None:
        logging.error(f"Failed to create privilege for {target_groupname}")
        return
    logging.info(f"Successfully created privilege for {target_groupname}")
    role_name = create_role_for_docker_group(target_groupname)
    if role_name is None:
        logging.error(f"Failed to create role for {target_groupname}")
        return
    logging.info(f"Successfully created role for {target_groupname}")
    returned_username = add_user_to_group(target_groupname, target_username)
    if returned_username is None:
        logging.error(f"Failed to update role for {target_groupname}")
        return
    logging.info(f"Successfully updated role for {target_groupname}")


# Create nexus role for the user
def create_role_for_docker_group(target_user_name):
    url = f"{nexus_url}/service/rest/v1/security/roles"
    role_name = f"nota-group-{target_user_name}"
    role_id = role_name
    privileges_ids = [f"docker-nota-group-{target_user_name}"]
    added_roles_ids = ["nota-common"]
    data = {
        "id": role_id,
        "name": role_name,
        "description": role_name,
        "privileges": privileges_ids,
        "roles": added_roles_ids
    }
    r = requests.post(url, json=data, auth=(nexus_username, nexus_password))
    logging.info(f"Status code for creating role for {target_user_name}: {r.status_code}")
    if r.status_code in [200, 201, 204]:
        logging.info(f"Successfully created role for {target_user_name}")
        return role_name
    else:
        logging.error(r.text)
        return None


# Update nexus role for the user
def add_user_to_group(target_group_name, target_user_name, account_source="LDAP"):
    group_role_name = f"nota-group-{target_group_name}"
    # Get user roles from user information
    url = f"{nexus_url}/service/rest/v1/security/users/?userId={target_user_name}"
    r = requests.get(url, auth=(nexus_username, nexus_password))
    logging.info(f"Status code for getting user information for {target_user_name}: {r.status_code}")
    if r.status_code not in [200, 201, 204]:
        logging.error(r.text)
        logging.error(f"Failed to get user information for {target_user_name}")
        return None
    user_info = json.loads(r.text)[0]
    user_roles = user_info["roles"]
    user_roles.append(group_role_name)
    data = {
        "userId": target_user_name,
        "source": account_source,
        "roles": user_roles,
        "lastName": target_user_name.split(".")[1],
        "firstName": target_user_name.split(".")[0],
        "emailAddress": user_info["emailAddress"],
        "status": "active"
    }
    url_for_updating_user = f"{nexus_url}/service/rest/v1/security/users/{target_user_name}"
    r = requests.put(url_for_updating_user, json=data, auth=(nexus_username, nexus_password))
    logging.info(f"Status code for updating role for {target_user_name}: {r.status_code}")
    if r.status_code in [200, 201, 204]:
        logging.info(f"Successfully updated role for {target_user_name}")
        return target_user_name
    else:
        logging.error(r.text)
        return None


def clear_group(group_name):
    # Delete role for the group
    target_role_name = f"nota-group-{group_name}"
    url = f"{nexus_url}/service/rest/v1/security/roles/{target_role_name}"
    r = requests.delete(url, auth=(nexus_username, nexus_password))
    logging.info(f"Status code for deleting role for {target_role_name}: {r.status_code}")
    if r.status_code in [200, 201, 204]:
        logging.info(f"Successfully deleted role for {target_role_name}")
    else:
        logging.error(r.text)

    # Delete privilege and content selector for the group
    target_groupname = f"docker-nota-group-{group_name}"
    url = f"{nexus_url}/service/rest/v1/security/privileges//{target_groupname}"
    r = requests.delete(url, auth=(nexus_username, nexus_password))
    logging.info(f"Status code for deleting privilege for {target_groupname}: {r.status_code}")
    if r.status_code in [200, 201, 204]:
        logging.info(f"Successfully deleted privilege for {target_groupname}")
    else:
        logging.error(r.text)

    url = f"{nexus_url}/service/rest/v1/security/content-selectors/{target_groupname}"
    r = requests.delete(url, auth=(nexus_username, nexus_password))
    logging.info(f"Status code for deleting content selector for {target_groupname}: {r.status_code}")
    if r.status_code in [200, 201, 204]:
        logging.info(f"Successfully deleted content selector for {target_groupname}")
    else:
        logging.error(r.text)


if __name__ == "__main__":
    # get_privileges()
    # get_content_selectors()
    target_group_name = args.target_group
    target_user_name = args.target_user

    #register_group("test-group", "sunjoo.park")
    #register_group(target_group_name, target_user_name)
    add_user_to_group(target_group_name, "sunjoo.park")
    #clear_group("test-group")
