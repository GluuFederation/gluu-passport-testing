# FILE for setting behave environment
# Currently supporting firefox

from selenium import webdriver
import os
from pyvirtualdisplay import Display
#import ldap

display = Display(visible=0, size=(1024, 768))

BEHAVE_DEBUG_ON_ERROR = False

def before_all(context):
    context.provider_host = os.getenv('PROVIDER_HOST')
    context.passport_host = os.getenv('PASSPORT_HOST')
    context.client_host = os.getenv('CLIENT_HOST')
    context.acr = os.getenv('ACR')
    context.requiring_email_profile = os.getenv('REQ_EMAIL_PROFILE')
    context.email_account_linking = os.getenv('EMAIL_ACCOUNT_LINKING')
    context.external_preselected_provider = os.getenv('EXT_PRESELECTED_PROVIDER')
    context.user_name=os.getenv('USER_NAME')
    context.user_password=os.getenv('USER_PASSWORD')
    context.flow=os.getenv('FLOW')
    context.user_mail = os.getenv('USER_MAIL')
    context.base_url = "https://" + context.client_host
    os.environ['CURL_CA_BUNDLE'] = ""
    context.SSL_verify = False
    display.start()


def before_scenario(context, scenario):
    options = webdriver.FirefoxOptions()
    options.headless = True
    context.web = webdriver.Firefox()

    # context.web = webdriver.Firefox()


def after_scenario(context, scenario):
    context.web.delete_all_cookies()
    context.web.close()


def after_step(context, step):
    print()
    if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
        # -- ENTER DEBUGGER: Zoom in on failure location.
        # NOTE: Use IPython debugger, same for pdb (basic python debugger).
        import ipdb
        ipdb.post_mortem(step.exc_traceback)


def after_all(context):
    pass
