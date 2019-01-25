from os import environ


def fetch_credentials():
    if 'SERVER_USERNAME' in environ:
        return prod_credentials()
    else:
        return dev_credentials()


def dev_credentials():
    return {"username": "DEV", "password": "DEV"}


def prod_credentials():
    return {"username": environ["SERVER_USERNAME"], "password": environ["SERVER_PASSWORD"]}
