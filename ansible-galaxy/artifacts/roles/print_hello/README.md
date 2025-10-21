# Ansible Role: print_hello

This is a simple Ansible role that prints a "hello" message.

## Role Variables

*   `user_name`: The name to be included in the hello message.
    *   Default: `"Sunjoo Park"`
    *   Example: `"World"`

## Example Playbook

Here is an example of how to use this role in a playbook:

```yaml
- hosts: localhost
  connection: local
  roles:
    - role: millvalley.dev_env.print_hello
      vars:
        user_name: "World"
```

This will print the message: `"print hello message: World"`.