import time
from selenium.webdriver.common.by import By
from behave import when, then, given
import requests
from selenium.common.exceptions import NoSuchElementException
import urllib3
from datetime import datetime

# in case of self-signed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def cookiesTransformer(sel_session_id, sel_other_cookies):
    ''' This transform cookies from selenium to requests '''
    s = requests.Session()
    s.cookies.set('session_id', sel_session_id)
    i = 0
    while i < len(sel_other_cookies):
        s.cookies.set(
            sel_other_cookies[i]['name'],
            sel_other_cookies[i]['value'],
            path=sel_other_cookies[i]['path'],
            domain=sel_other_cookies[i]['domain'],
            secure=sel_other_cookies[i]['secure'],
            rest={'httpOnly': sel_other_cookies[i]['httpOnly']}
        )
        i = i+1

    return s


def getIdpInitiatedLink(context):
    return 'https://%s/idp/profile/SAML2/Unsolicited/SSO?providerId=%s&target=%s/protected-content' % (
        context.provider_host, context.client_host, context.base_url)


@given(u'that user exists in provider')
def user_exists(context):
    assert context.user_name is not None


@given(u'user is authenticated')
def user_authenticates(context):
    if context.flow == 'idp-initiated':
        context.web.get(getIdpInitiatedLink(context))
    else:
        context.web.get(context.base_url+"/login")

    time.sleep(3)

    if context.acr == "passport-saml":

        # for all samls..
        time.sleep(2)
        context.web.save_screenshot(
            str(datetime.now())+"3_before_username_typing.png")
        context.web.find_element(By.ID, "username").click()
        context.web.find_element(
            By.ID, "username").send_keys(context.user_name)
        context.web.find_element(By.ID, "password").send_keys(
            context.user_password)
        context.web.save_screenshot(
            str(datetime.now())+"4_before_login_button.png")
        context.web.find_element(By.ID, "loginButton").click()

        time.sleep(3)
        context.web.save_screenshot(
            str(datetime.now())+"5_after_login_button.png")

        try:
            context.web.find_element(
                By.ID, "authorizeForm:allowButton").click()
        except NoSuchElementException:
            # Couldn't find consent form, presuming user already consented...
            pass

        time.sleep(2)

        if context.flow == "default emailreq":
            # should ask for e-mail input
            context.web.save_screenshot(
                str(datetime.now())+"6_before_enter_email.png")
            time.sleep(5)

            try:
                context.web.find_element(
                    By.ID, "loginForm:email").send_keys(context.user_mail)
                context.web.save_screenshot(
                    str(datetime.now())+"7_after_enter_email.png")
                context.web.find_element(By.ID, "loginForm:j_idt14").click()
                time.sleep(2)
                context.web.save_screenshot(
                    str(datetime.now())+"8_after_click_login_button.png")
            except NoSuchElementException:
                # Couldn't find email form, presuming user formerly entered...
                pass
            try:
                context.web.find_element(
                    By.ID, "authorizeForm:allowButton").click()
            except NoSuchElementException:
                pass
                # "Couldn't find consent form, presuming user already consented...")

        time.sleep(2)

        time.sleep(2)
        # print(context.web.current_url)

    if context.acr == "oidc":

        time.sleep(1)
        context.web.set_window_size(625, 638)
        context.web.find_element(By.ID, "username").click()
        context.web.find_element(By.ID, "username").send_keys(context.username)
        time.sleep(2)
        context.web.find_element(By.ID, "password").send_keys(
            context.user_password)
        context.web.find_element(By.ID, "loginButton").click()
        time.sleep(2)

    assert context.web.current_url.startswith(context.base_url)
    context.web.save_screenshot(str(datetime.now())+"_authenticated.png")
    time.sleep(2)


@when(u'user tries to access protected content page')
def user_clicks_protected_content_link(context):
    if context.flow == 'idp-initiated':
        # acessing idp init link instead of demo app protected content.
        context.web.get(getIdpInitiatedLink(context))
    else:
        context.web.get(context.base_url)
        time.sleep(2)
        context.web.find_element_by_xpath(
            '//a[@href="'+context.base_url+"/protected-content"+'"]').click()
        context.has_clicked = True
    time.sleep(2)


@then(u'user should be redirected to login page')
def user_redirected_to_external_login_page(context):
    external_login_page = None
    if context.acr == 'passport-saml':

        # if context.flow != 'preselected provider':
        #     external_login_page = "https://%s/oxauth/authorize.htm" % context.passport_host
        # else:
        external_login_page = "https://%s/oxauth/login" % context.provider_host
        time.sleep(4)
        #import ipdb; ipdb.set_trace()
    else:
        external_login_page = "https://%s/oxauth/login" % context.passport_host
    time.sleep(4)

    selenium_url = context.web.current_url
    assert selenium_url.startswith(external_login_page)


@then(u'user should access protected content')
def user_access_protected_content(context):
    # We fetch cookies from selenium and pass them through request to validate
    new_sess = cookiesTransformer(
        context.web.session_id, context.web.get_cookies())
    res = new_sess.get(context.base_url + "/protected-content", verify=False)

    assert res.url == context.base_url + "/protected-content"
    context.web.save_screenshot(str(datetime.now())+"_protected-content.png")
