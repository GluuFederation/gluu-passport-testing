from ldaphelper import TrustRelationships, LdapConnector

connector = LdapConnector('cn=directory manager','Test123$')
trs = TrustRelationships(connector)

tr = trs.get_tr_by_display_name('saml-default')
import ipdb; ipdb.set_trace()
# trs.test_upload()

