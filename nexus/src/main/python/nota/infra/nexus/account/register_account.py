import requests
import argparse
import os
import logging

logging.getLogger().setLevel(logging.INFO)

# Get username and password from arguments
parser = argparse.ArgumentParser()
parser.add_argument("--username", required=True)
parser.add_argument("--password", required=True)
parser.add_argument("--url", required=True)
parser.add_argument("--target_user", required=True)
parser.add_argument("--clear", action="store_true", default=False)
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


def create_content_selector_for_docker_personal(target_user_name):
    url = f"{nexus_url}/service/rest/v1/security/content-selectors"
    cs_name = f"docker-nota-people-{target_user_name}"
    cs_expression = f"format == \"docker\" and path =^ \"/v2/nota/people/{target_user_name}/\""
    data = {
        "name": cs_name,
        "description": cs_name,
        "expression": cs_expression,
        "enabled": True
    }
    r = requests.post(url, json=data, auth=(nexus_username, nexus_password))
    logging.info(f"Status code for creating content selector for {target_user_name}: {r.status_code}")
    if r.status_code in [200, 201, 204]:
        logging.info(f"Successfully created content selector for {target_user_name}")
        return cs_name
    else:
        logging.error(r.text)
        return None


# Create privilege for the user
def create_privilege_for_docker_personal(target_user_name):
    url = f"{nexus_url}/service/rest/v1/security/privileges/repository-content-selector"
    privilege_name = f"docker-nota-people-{target_user_name}"
    data = {
        "name": privilege_name,
        "description": privilege_name,
        "actions": ["ALL"],
        "format": "docker",
        "repository": "*",
        "contentSelector": f"docker-nota-people-{target_user_name}",
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
def register_account(target_username):
    cs_name = create_content_selector_for_docker_personal(target_username)
    if cs_name is None:
        logging.error(f"Failed to create content selector for {target_username}")
        return
    logging.info(f"Successfully created content selector for {target_username}")
    privilage_name = create_privilege_for_docker_personal(target_username)
    if privilage_name is None:
        logging.error(f"Failed to create privilege for {target_username}")
        return
    logging.info(f"Successfully created privilege for {target_username}")
    role_name = create_role_for_docker_personal(target_username)
    if role_name is None:
        logging.error(f"Failed to create role for {target_username}")
        return
    logging.info(f"Successfully created role for {target_username}")
    returned_username = update_role_for_user(target_username)
    if returned_username is None:
        logging.error(f"Failed to update role for {target_username}")
        return
    logging.info(f"Successfully updated role for {target_username}")


# Create nexus role for the user
def create_role_for_docker_personal(target_user_name):
    url = f"{nexus_url}/service/rest/v1/security/roles"
    role_name = f"nota-people-{target_user_name}"
    role_id = f"nota-people-{target_user_name}"
    privileges_ids = [f"docker-nota-people-{target_user_name}"]
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
def update_role_for_user(target_user_name, account_source="LDAP"):
    url = f"{nexus_url}/service/rest/v1/security/users/{target_user_name}"
    user_roles = [f"nota-people-{target_user_name}"]
    data = {
        "userId": target_user_name,
        "source": account_source,
        "roles": user_roles,
        "lastName": target_user_name.split(".")[1],
        "firstName": target_user_name.split(".")[0],
        "emailAddress": target_user_name + "@nota.ai",
        "status": "active"
    }
    r = requests.put(url, json=data, auth=(nexus_username, nexus_password))
    logging.info(f"Status code for updating role for {target_user_name}: {r.status_code}")
    if r.status_code in [200, 201, 204]:
        logging.info(f"Successfully updated role for {target_user_name}")
        return target_user_name
    else:
        logging.error(r.text)
        return None


def clear_account(user_name):
    # Remove all roles from the user
    url = f"{nexus_url}/service/rest/v1/security/users/{user_name}"
    data = {
        "userId": user_name,
        "source": "LDAP",
        "roles": ["nx-anonymous"],
        "privileges": [],
        "lastName": user_name.split(".")[1],
        "firstName": user_name.split(".")[0],
        "emailAddress": user_name + "@nota.ai",
        "status": "active"
    }

    r = requests.put(url, json=data, auth=(nexus_username, nexus_password))
    logging.info(f"Status code for removing roles from {user_name}: {r.status_code}")
    if r.status_code in [200, 201, 204]:
        logging.info(f"Successfully removing roles from {user_name}")
    else:
        logging.error(r.text)

    # Delete role for the user
    target_role_name = f"nota-people-{user_name}"
    url = f"{nexus_url}/service/rest/v1/security/roles/{target_role_name}"
    r = requests.delete(url, auth=(nexus_username, nexus_password))
    logging.info(f"Status code for deleting role for {target_role_name}: {r.status_code}")
    if r.status_code in [200, 201, 204]:
        logging.info(f"Successfully deleted role for {target_role_name}")
    else:
        logging.error(r.text)

    # Delete privilege and content selector for the user
    target_username = f"docker-nota-people-{user_name}"
    url = f"{nexus_url}/service/rest/v1/security/privileges//{target_username}"
    r = requests.delete(url, auth=(nexus_username, nexus_password))
    logging.info(f"Status code for deleting privilege for {target_username}: {r.status_code}")
    if r.status_code in [200, 201, 204]:
        logging.info(f"Successfully deleted privilege for {target_username}")
    else:
        logging.error(r.text)

    url = f"{nexus_url}/service/rest/v1/security/content-selectors/{target_username}"
    r = requests.delete(url, auth=(nexus_username, nexus_password))
    logging.info(f"Status code for deleting content selector for {target_username}: {r.status_code}")
    if r.status_code in [200, 201, 204]:
        logging.info(f"Successfully deleted content selector for {target_username}")
    else:
        logging.error(r.text)


if __name__ == "__main__":
    # get_privileges()
    # get_content_selectors()
    if not args.clear:
        logging.info(f"Registering account for {args.target_user}")
        register_account(args.target_user)
    else:
        logging.info(f"Clearing account for {args.target_user} from nexus")
        clear_account(args.target_user)
