# Start configuring and insert data into ldap
# Insert and manage all data operations for passport provider host
import os
from utils.utils import Utils

# Values
ldap_hostname = os.environ.get('LDAP_HOSTNAME') or 'localhost'
ldaps_port = os.environ.get('LDAP_PORT') or '1636'
ldap_pass = os.environ.get('LDAP_PASS') or os.environ.get('PASSPORT_HOST_GLUU_ADMIN_PASSWORD')
ldap_binddn = 'cn=directory manager'
passport_host = os.environ.get('PASSPORT_HOST')
provider_host = os.environ.get('PROVIDER_HOST')
client_host = os.environ.get('CLIENT_HOST')

# Init utils
utils = Utils(ldap_hostname, ldaps_port, ldap_pass, ldap_binddn)

# Connect ldap
utils.connect_db()

# enable passport social and saml script
# 2FDB-CF02 - passport_social
# D40C-1CA4 - passport_saml
# 2DAF-F9A5 - scim_access_policy
for inum in ['2FDB-CF02', 'D40C-1CA4', '2DAF-F9A5']:
  utils.enable_script(inum)

# import passport config and providers
test_dir = os.environ.get('TEST_DIR')
passport_ldifs_dir = '{}/data/ldifs/passport_host'.format(test_dir)
passport_config_file = '{}/gluuPassportConfiguration.json'.format(passport_ldifs_dir)
passport_ldif_file = '{}/passport.ldif'.format(passport_ldifs_dir)

oxauth_dynamic_config_file = '{}/oxauthDynamicConfig.json'.format(passport_ldifs_dir)
oxauth_ldif_file = '{}/oxauth.ldif'.format(passport_ldifs_dir)
passport_saml_scripts_ldif_file = '{}/passport_saml_scripts.ldif'.format(passport_ldifs_dir)
passport_social_scripts_ldif_file = '{}/passport_social_scripts.ldif'.format(passport_ldifs_dir)

# fetch idp cert
idp_cert = utils.get_idp_signing_cert(provider_host)

## Gluu Passport Config setup
# populate passport json config
passport_config_props = {
  "passport_host": passport_host,
  "provider_host": provider_host,
  "idp_cert": idp_cert,
  "client_host": client_host
}
utils.populate_file(passport_config_file, passport_config_props , is_file_json=True)

# remove extra new lines from json config
passport_file_text = utils.get_file_data(passport_config_file).replace('\n', '')
gluu_passport_configuration = passport_file_text
utils.populate_file(passport_ldif_file, { "gluu_passport_configuration": gluu_passport_configuration })

## oxAuth dynamic config setup
# add authorizationRequestCustomAllowedParameters: preselectedExternalProvider
utils.populate_file(oxauth_dynamic_config_file, { "passport_host": passport_host } , is_file_json=True)

# remove extra new lines from json config
oxauth_dynamic_config_file_text = utils.get_file_data(oxauth_dynamic_config_file).replace('\n', '')
oxauth_dynamic_config = oxauth_dynamic_config_file_text.replace('\n', '')
utils.populate_file(oxauth_ldif_file, { "oxauth_dynamic_config": oxauth_dynamic_config })

utils.import_ldif([passport_ldif_file, oxauth_ldif_file, passport_saml_scripts_ldif_file, passport_social_scripts_ldif_file])
