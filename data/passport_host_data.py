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
idp_host = os.environ.get('IDP_HOST')

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
pasport_ldifs_dir = '{}/data/ldifs/passport_host'.format(test_dir)
passport_config_file = '{}/gluuPassportConfiguration.json'.format(pasport_ldifs_dir)
passport_ldif_file = '{}/passport.ldif'.format(pasport_ldifs_dir)

# fetch idp cert
idp_cert = utils.get_idp_signing_cert(idp_host)

# populate passport json config
passport_config_props = {
  "passport_host": passport_host,
  "idp_host": idp_host,
  "idp_cert": idp_cert
}
utils.populate_file(passport_config_file, passport_config_props , is_file_json=True)

# remove extra new lines from json config
with open(passport_config_file) as f:
  passport_file_text = f.read()

gluu_passport_configuration = passport_file_text.replace('\n', '')

# populate passport ldif
utils.populate_file(passport_ldif_file, { "gluu_passport_configuration": gluu_passport_configuration })

# import passport config and providers
utils.import_ldif([passport_ldif_file])
