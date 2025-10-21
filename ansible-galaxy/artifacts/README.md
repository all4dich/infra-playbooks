# Ansible Collection: millvalley.dev_env

This directory contains an Ansible collection named `millvalley.dev_env`.

## Contents

*   `galaxy.yml`: Contains metadata for the collection, such as namespace, name, version, and authors.
*   `playbooks/`: Contains example playbooks that demonstrate how to use the roles within this collection.
    *   `print_hello.yml`: A simple playbook that uses the `print_hello` role.
    *   `universe.yml`: A playbook that sets up a development environment using the `nvim` and `build_tools` roles.
*   `roles/`: Contains the Ansible roles for this collection.
    *   `build_tools`: Installs essential build tools.
    *   `nvim`: Installs Neovim.
    *   `print_hello`: A simple role that prints a hello message.
