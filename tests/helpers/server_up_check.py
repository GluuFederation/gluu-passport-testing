# helper to wait server up
import os
import requests
import time

server = os.getenv("PASSPORT_HOST")


def is_up(server):
    """Returns true if server is up

    :param server: server host addr (without https)
    :type server: str
    :return: True if is up, False if not returning 200
    :rtype: bool
    """
    try:
        response = requests.get('https://' + server)
        return bool(response.status_code == 200)
    except Exception as e:
        print(e)
        return False


def wait_till_up(server):
    is_server_up = is_up(server)
    while not is_server_up:
        print('Server still not ready...')
        time.sleep(10)
        is_server_up = is_up(server)
    print('Server is UP!')


wait_till_up(server)
