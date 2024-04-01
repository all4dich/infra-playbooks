import requests
import os


username = os.environ['NEXUS_USERNAME']
password = os.environ['NEXUS_PASSWORD']


def delete_content_selector(name):
    url = f"https://registry.nota.ai/service/rest/v1/security/content-selectors/{name}"
    r = requests.delete(url, auth=(username, password), verify=False)
    print(r.text)

def create_content_selector(name, expression):
    url = "https://registry.nota.ai/service/rest/v1/security/content-selectors"
    data = {
        "name": name,
        "description": name,
        "expression": expression,
        "enabled": True
    }
    r = requests.post(url, json=data, auth=(username, password), verify=False)
    print(r.text)

def get_all_content_selectors():
    url = "https://registry.nota.ai/service/rest/v1/security/content-selectors"
    r = requests.get(url, auth=(username, password), verify=False)
    print(r.text)

name = "keonyul.park"
cs_name = f"docker-nota-people-{name}"
cs_expression = f"format == \"docker\" and path =^ \"/v2/nota/people/{name}/\""
create_content_selector(cs_name, cs_expression)
#delete_content_selector(cs_name)
get_all_content_selectors()