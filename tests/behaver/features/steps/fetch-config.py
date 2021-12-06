import socket
from tests.helpers.utils import run_command
from behave import when, then, given
import time
from selenium.webdriver.common.by import By
import subprocess
from datetime import datetime

def check_string_in_file(file_path, searchText):
    with open(file_path) as f:
        found = searchText in f.read()
        f.close()
        return found

@given(u'passport is not running')
def check_passport_is_not_running(context):
    context.web.get("https://%s/passport/health-check" % context.test_server_host)
    context.web.save_screenshot(str(datetime.now())+"after_health_check.png")
    responseMessage = context.web.find_element(By.TAG_NAME, "p").text
    assert "503" in responseMessage

@given(u'oxauth is running')
def check_oxauth_is_running(context):
    context.web.get("https://%s" % context.test_server_host)
    time.sleep(2)
    context.web.save_screenshot(str(datetime.now())+"check_oxauth_is_running.png")
    loginButton = context.web.find_element(By.ID, "loginForm:loginButton")
    assert "Login" in loginButton.get_attribute("value")

@when(u'passport is started')
def start_passport(context):
    run_command('''ssh -o IdentityFile=/etc/gluu/keys/gluu-console \
        -o Port=60022  \
        -o StrictHostKeyChecking=no \
        -o UserKnownHostsFile=/dev/null \
        -o PubkeyAuthentication=yes \
        root@localhost \
        "service passport start"''')
    time.sleep(2)

@when(u'wait for the fetch configuration time')
def wait_to_fetch_config(context):
    context.web.get("https://%s/passport/health-check" % context.test_server_host)
    time.sleep(2)
    context.web.save_screenshot(str(datetime.now())+"after_health_check2_fetched.png")
    responseMessage = context.web.find_element(By.ID, "/message").text
    assert "Cool" in responseMessage

@then(u'configuration should be correctly fetched')
def check_configuration_fetch_or_not(context):
    assert check_string_in_file(context.passport_log_file, 'Passport configs received')
