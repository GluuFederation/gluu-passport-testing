import time
from selenium.webdriver.common.by import By
from behave import when, then, given
import urllib3
from datetime import datetime

# in case of self-signed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@given(u'user never authenticated before')
def user_exists(context):
    assert context.user_name is not None


@given(u'user started inbound authentication flow')
def user_authenticates(context):
    context.web.get(context.base_url+"/login")

    time.sleep(3)

    context.web.set_window_size(625, 638)
    context.web.find_element(By.ID, "username").click()
    context.web.find_element(By.ID, "username").send_keys(context.username)
    time.sleep(2)
    context.web.find_element(By.ID, "password").send_keys(
        context.user_password)
    context.web.find_element(By.ID, "loginButton").click()
    time.sleep(2)

@when(u'user deny consent')
def user_deny_consent(context):
    # deny consent
    context.web.find_element(
                By.ID, "authorizeForm:doNotAllowButton").click()

    assert context.web.current_url.startswith(context.base_url)
    context.web.save_screenshot(str(datetime.now())+"_deny_consent.png")

@then(u'user should be redirected to login page')
def user_redirected_to_external_login_page(context):
    external_login_page = "https://%s/oxauth/login" % context.passport_host
    time.sleep(4)
    context.web.save_screenshot(str(datetime.now())+"_login_screen_after_deny.png")

    selenium_url = context.web.current_url
    assert selenium_url.startswith(external_login_page)
