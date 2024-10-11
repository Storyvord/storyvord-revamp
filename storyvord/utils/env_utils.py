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

def get_site_url(default=None):
    """
    Retrieves the site url and sets tha correct environment.
    """
    value = os.getenv('SITE')
    if value is not None:
        if value.lower() == 'dev':
            return 'https://dev.storyvord.com'
        elif value.lower() == 'stage':
            return 'https://stage.storyvord.com'
        elif value.lower() == 'production':
            return 'https://storyvord.com'
        else:
            return 'http://localhost:8000'
    return default