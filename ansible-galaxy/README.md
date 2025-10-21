# Ansible Playbooks for Development Environment

This repository contains examples for Ansible playbooks and roles to configure a development environment.

## Structure

*   `ansible.cfg`: Ansible configuration file.
*   `ansible_galaxy_requirements.yml`: Defines collection dependencies, pointing to the local `artifacts` directory.
*   `docker-compose.yaml`, `Dockerfile`, `Dockerfile-target`: Docker setup for creating and testing the Ansible environment.
*   `artifacts/`: Contains a distributable Ansible collection named `millvalley.dev_env`.
*   `playbooks/`: Contains operational playbooks for tasks like checking the system, managing files, and enabling remote user environments.
*   `temp/`: Contains temporary and example playbooks demonstrating various Ansible features.

## How to Use

This project is set up to be used with Docker.

1.  **Build and run the containers:**
    ```bash
    docker-compose up -d
    ```
2.  **Access the Ansible container:**
    ```bash
    docker-compose exec ansible_galaxy bash
    ```
3.  **Run playbooks:**
    From within the `ansible_galaxy` container, you can run the provided playbooks. For example:
    ```bash
    pushd /workspace/ansible-galaxy/
    ansible-galaxy collection install -f -r ./ansible_galaxy_requirements.yml 
    ansible-playbook millvalley.dev_env.print_hello
    ```
