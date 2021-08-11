import socket
import time

def check_port_running(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    res = sock.connect_ex(('localhost', port))
    sock.close()
    return res == 0

def check_string_in_file(file_path, searchText):
    with open(file_path) as f:
        found = searchText in f.read()
        f.close()
        return found

@given(u'passport is not running')
def check_passport_is_not_running(context):
    assert not check_port_running(context.passport_port)

@given(u'oxauth is running')
def check_oxauth_is_running(context):
    assert check_port_running(context.oxauth_port)

@when(u'passport is started')
def check_passport_is_running(context):
    assert check_port_running(context.passport_port)

@when(u'wait for the fetch configuration time')
def wait_to_fetch_config():
    time.sleep(6)

@then(u'configuration should be correctly fetched')
def check_configuration_fetch_or_not(context):
    assert check_string_in_file(context.passport_log_file, 'Passport configs received')