# Ansible
This file shows how you can use Nota ansible playbooks to manage company infrastructures

## Prerequites
* Before using playbooks, you have you set these environment variables
```shell
export ANSIBLE_USERNAME=dev
export ANSIBLE_PASSWORD=xxxxxxxxxxxxxx
export ANSIBLE_BECOME_PASSWORD=xxxxxxxxxxxxxxxxx
```
## Server Management
### User Management
* Create a one user. A user will be received a mail that have user password and new ssh private key.
```shell
ansible-playbook -i inventory/all-servers.yaml \
--extra-vars "target_password=$(LC_ALL=C tr -dc "a-zA-Z0-9-_\$\?" < /dev/urandom | head -c 10)" \
playbooks/create-one-user.yaml
```
* Create a one user without any interactions.  A user will be received a mail that have user password and new ssh private key. 
```shell
ansible-playbook -i inventory/all-servers.yaml \
--extra-vars "target_host=3090b user_name=soyul.park user_email=sunjoo.park@nota.ai user_home=/ssd1/soyul.park target_password=$(LC_CTYPE=C tr -dc "a-zA-Z0-9-_\$\?" < /dev/urandom | head -c 10) "  playbooks/create-one-user.yaml
```
* Remove a one user from the host
```shell
ansible-playbook -i inventory/all-servers.yaml --extra-vars "target_host=3090b user_name=soyul.park" \
playbooks/remove-one-user.yaml
```
* Reset a password and register a new ssh key
```shell
ansible-playbook -i inventory/all-servers.yaml \
--extra-vars "target_host=3090b target_user=soyul.park user_email=sunjoo.park@nota.ai target_password=$(LC_CTYPE=C tr -dc "a-zA-Z0-9-_\$\?" < /dev/urandom | head -c 10)" playbooks/reset-user-password-and-key.yaml
```

