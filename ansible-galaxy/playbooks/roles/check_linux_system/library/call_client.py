#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule

def main():
    # Define any arguments your module might accept (even if none)
    module_args = dict(
        user_name=dict(type='str', required=True),
        user_location=dict(type='str', required=False, default='default_value')
    )
    # Create the module object
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True  # Good practice
    )

    # --- Your module's logic goes here ---
    # For this example, we just set a message.
    p1 = module.params['user_name']
    p2 = module.params['user_location']

    # -------------------------------------

    # Prepare the result dictionary to send back
    result = {
        "changed": False,  # Set to True if your module made a change
        "msg": "Hello from call_client.py : " + p1,
        "user_name": p1,
        "user_location": p2
    }

    # This function correctlyf ormats and exits with the JSON result
    module.exit_json(**result)


if __name__ == '__main__':
    main()
