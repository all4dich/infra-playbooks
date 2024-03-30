# Ansible
This file shows how you can use Nota ansible playbooks to manage company infrastructures

## Prerequites
* Before using playbooks, you have you set these environment variables
```shell
export ANSIBLE_USERNAME=dev
export ANSIBLE_PASSWORD=xxxxxxxxxxxxxx
export ANSIBLE_BECOME_PASSWORD=xxxxxxxxxxxxxxxxx
export SMTP_USERNAME=xxxxxxxxxxxxxxxxxxxxx
export SMTP_PASSWORD=xxxxxxxxxxxxxxxxxxxxxxx
export SMTP_HOST=email-smtp.ap-northeast-2.amazonaws.com
```
Some scripts send a mail to a user for let a user know the result. Emails will be delivered to a user via Amazon SES.
## Server Management
### General
#### Upload local artifacts to remote servers
Run copy_artifacts.yaml like this 
```shell
ansible-playbook -i inventory/all-servers.yaml playbooks/copy_artifacts.yaml -e hosts=eve -e owner=dev -e group=root -e source=/Users/sunjoo/test.yaml -
```
### User Management
#### Create User Account
* Create a one user. A user will be received a mail that have user password and new ssh private key.
```shell
ansible-playbook -i inventory/all-servers.yaml playbooks/create-one-user.yaml
```
* Create a one user without any interactions.  A user will be received a mail that have user password and new ssh private key. 
```shell
ansible-playbook -i inventory/all-servers.yaml \
--extra-vars "target_host=3090b user_name=soyul.park user_email=sunjoo.park@nota.ai user_home=/ssd1/soyul.park"  \
playbooks/create-one-user.yaml
```
If you set 'all' for target_host, all servers that are described on 'inventory/all-servers' will create an account with same password and key file.
#### Update an account information
* Remove a one user from the host
```shell
ansible-playbook -i inventory/all-servers.yaml --extra-vars "target_host=3090b user_name=soyul.park" playbooks/remove-one-user.yaml
```
* Reset a password and register a new ssh key
```shell
ansible-playbook -i inventory/all-servers.yaml \
--extra-vars "target_host=3090b target_user=soyul.park user_email=sunjoo.park@nota.ai" playbooks/reset-user-password-and-key.yaml
```
If you set 'all' for target_host, an account on each server will use saame password and key file.
* Register a ssh key for user
```shell
ansible-playbook -i inventory/all-servers.yaml playbooks/register-user-ssh-key.yaml --extra-vars "target_host=3090a target_user=sunjoo.park user_email=sunjoo.park@nota.ai"
```
* Reset a password
```shell
ansible-playbook -i inventory/all-servers.yaml playbooks/reset-user-password.yaml --extra-vars "target_host=all target_user=sunjoo.park target_password=$(LC_CTYPE=C tr -dc "a-zA-Z0-9-_\$\?" < /dev/urandom | head -c 10)"
```

