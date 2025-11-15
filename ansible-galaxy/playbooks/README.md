# Operational Playbooks

This directory contains Ansible playbooks for various operational tasks.

## Playbooks

*   `check-linux-system.yml`: This playbook checks if essential editor tools like `emacs` and `vim` are installed on the target host. It uses the `check_linux_editor_tools` role.
*   `check_file_manage.yml`: This playbook creates a file on the target host and then lists the contents of the `/tmp/` directory to verify its creation. It uses the `create_file` role.
*   `enable-remote-user-env.yml`: This playbook is designed to upload an SSH public key to a remote host to enable passwordless authentication. It uses the `upload_ssh_public_key` role.
