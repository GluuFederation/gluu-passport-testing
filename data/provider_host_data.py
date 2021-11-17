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

# import idp users and trust relationship data
test_dir = os.environ.get('TEST_DIR')
provider_ldifs_dir = '{}/data/ldifs/provider_host'.format(test_dir)
tr_file = '{}/trust_relationships.ldif'.format(provider_ldifs_dir)
people_ldif_file = '{}/peoples.ldif'.format(provider_ldifs_dir)
passport_saml_ldif_file = '{}/passport_saml.ldif'.format(provider_ldifs_dir)

# populate tr ldif
utils.populate_file(tr_file, { "passport_host": passport_host })

# import tr and users
utils.import_ldif([tr_file, people_ldif_file, passport_saml_ldif_file])
