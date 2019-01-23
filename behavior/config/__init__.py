import os


def fetch_credentials():
    if 'USERNAME' in os.environ:
        from . import prod
        return prod.get_credentials()
    else:
        from . import dev
        return dev.get_credentials()
