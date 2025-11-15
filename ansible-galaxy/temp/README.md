# Temporary and Example Playbooks

This directory is used for temporary files, experiments, and examples to demonstrate various Ansible features. The playbooks and roles in this directory are for educational and testing purposes and are not part of the main application.

## Contents

This directory contains a variety of playbooks and roles that showcase different Ansible functionalities:

*   `main.yml`: Demonstrates static and dynamic task imports (`import_tasks`, `include_tasks`), loops, handlers, and including/importing roles.
*   `main2.yml`: Shows how to use roles, including duplicate roles.
*   `main_check_vars.yml`: An example of using `vars_files` to load variables.
*   `playbook_1.yml` and `playbook_2.yml`: Simple playbooks used for demonstrating playbook imports.
*   `common_tasks.yml` and `look_tasks.yml`: Files containing tasks that are included in other playbooks.
*   `roles/`: Contains example roles (`common`, `common_import`, `foo`) to demonstrate role dependencies and execution.
*   `vars/`: Contains an example variables file (`main.yml`).