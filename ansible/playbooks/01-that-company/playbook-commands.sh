# List of command
1. Create one user 
ansible-playbook -i inventory/all-servers.yaml --extra-vars "target_password=$(LC_ALL=C tr -dc "a-zA-Z0-9-_\$\?" < /dev/urandom | head -c 10)" playbooks/create-one-user.yaml 

2. Create one user without interactions
ansible-playbook -i inventory/all-servers.yaml --extra-vars "target_host=3090b user_name=soyul.park user_email=sunjoo.park@nota.ai user_home=/ssd1/soyul.park target_password=$(LC_CTYPE=C tr -dc "a-zA-Z0-9-_\$\?" < /dev/urandom | head -c 10) "  playbooks/create-one-user.yaml

3. Remove a user from hosts
ansible-playbook -i inventory/all-servers.yaml --extra-vars "target_host=3090a user_name=soyul.park user_email=sunjoo.park@nota.ai"  playbooks/remove-one-user.yaml

# Sample commands
    - ansible-playbook -i inventory/all-servers.yaml --extra-vars "target_host=3090d target_user=test.user user_email=sunjoo.park@nota.ai target_password=$(openssl rand -base64 10)"  playbooks/reset-user-password-and-key.yaml
    - ansible-playbook -i inventory/all-servers.yaml --extra-vars "target_host=3090d user_name=test.user user_email=sunjoo.park@nota.ai user_home=/ssd1/test.user target_password=$(openssl rand -base64 10) "  playbooks/create-one-user.yaml
    - ansible-playbook -i inventory/all-servers.yaml --extra-vars "target_host=3090d user_name=test.user user_email=sunjoo.park@nota.ai user_home=/ssd1/test.user "  playbooks/remove-one-user.yaml
    - A=$(LC_CTYPE=C tr -dc "a-zA-Z0-9-_\$\?" < /dev/urandom | head -c 10)
    - ansible-playbook -i inventory/all-servers.yaml --extra-vars "target_host=3090d user_name=test.user user_email=sunjoo.park@nota.ai user_home=/ssd1/test.user target_password=$(LC_CTYPE=C tr -dc "a-zA-Z0-9-_\$\?" < /dev/urandom | head -c 10) "  playbooks/create-one-user.yaml
    - ansible-playbook -i inventory/all-servers.yaml --extra-vars "target_host=3090d user_name=test.user user_email=sunjoo.park@nota.ai user_home=/ssd1/test.user target_password=$(LC_ALL=C tr -dc "a-zA-Z0-9-_\$\?" < /dev/urandom | head -c 10) "  playbooks/create-one-user.yaml