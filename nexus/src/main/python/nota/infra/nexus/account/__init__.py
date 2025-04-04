import requests
import logging


class NexusConnector:
    def __init__(self, account="", password="", url=""):
        self.account = account
        self.password = password
        self.url = url

    def add_privileges_to_roles(self, roles, privileges):
        for role in roles:
            url = f"{self.url}/service/rest/v1/security/roles/{role}"
            r = requests.get(url, auth=(self.account, self.password))
            logging.info(f"Status code for getting role info named as {role}: {r.status_code}")
            if r.status_code in [200, 201, 204]:
                role_id = r.json()["id"]
                privileges_old = r.json()["privileges"]
                privileges_new = list(set(privileges_old + privileges))
                data = {
                    "id": role_id,
                    "name": role_id,
                    "privileges": privileges_new,
                    "roles": r.json()["roles"]
                }
                logging.info(data)
                logging.info(f"New privileges for role {role}: {privileges_new}")
                r_put = requests.put(url, json=data, auth=(self.account, self.password))
                logging.info(f"Status code for adding privilege to role {role}: {r_put.status_code}")
                if r_put.status_code in [200, 201, 204]:
                    logging.info(f"Successfully added privileges to role {role}")
                else:
                    logging.error(r_put.text)
            else:
                logging.error(r.text)

    def get_role_info(self, role):
        url = f"{self.url}/service/rest/v1/security/roles/{role}"
        r = requests.get(url, auth=(self.account, self.password))
        logging.info(f"Status code for getting role info for {role}: {r.status_code}")
        if r.status_code == 200:
            return r.json()
        else:
            logging.error(r.text)
            return None
