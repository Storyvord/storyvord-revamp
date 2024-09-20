# utils/env_utils.py

import os

def get_bool_env_var(var_name, default=False):
    """
    Retrieves an environment variable and converts it to a boolean.
    """
    value = os.getenv(var_name)
    if value is not None:
        return value.lower() in ('true', '1', 't', 'yes')
    return default
