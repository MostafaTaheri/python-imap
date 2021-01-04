import logging
import os

import yaml

from imap.email import Email


def load_config():
    config_file = os.environ.get('CONFIG', None)
    stream = open(
        config_file if config_file[0] == '/' else os.path.join(
            os.path.dirname(__file__), config_file), 'r')
    config = yaml.safe_load_all(stream)
    return config


def imap_email(config):
    """Reads email."""
    try:
        email = Email()
        for handler in config['handlers']:
            email = email(handler=handler)
    except Exception as Exp:
        logging.exception(Exp)


if __name__ == '__main__':
    config = load_config()
    imap_email(config=config)
