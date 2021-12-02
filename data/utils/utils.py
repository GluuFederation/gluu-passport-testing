import ldap3
from utils import ldif_utils
from xml.dom import minidom
from urllib import request

class Utils:

  def __init__(self, ldap_hostname, ldaps_port, ldap_pass, ldap_binddn):
    """ldap and other utilities"""
    self.ldap_hostname = ldap_hostname
    self.ldaps_port = ldaps_port
    self.ldap_pass = ldap_pass
    self.ldap_binddn = ldap_binddn

  def connect_db(self, use_ssl=True, force=False):
    print("Bind to database")
    print("Making LDAP Conncetion")
    ldap_server = ldap3.Server(self.ldap_hostname, port=int(self.ldaps_port), use_ssl=use_ssl)
    self.ldap_conn = ldap3.Connection(
                ldap_server,
                user=self.ldap_binddn,
                password=self.ldap_pass,
                )
    print("Making LDAP Connection to host {}:{} with user {}".format(self.ldap_hostname, self.ldaps_port, self.ldap_binddn))
    self.ldap_conn.bind()

  def enable_script(self, inum):
    ldap_operation_result = self.ldap_conn.modify(
      'inum={},ou=scripts,o=gluu'.format(inum),
      {"oxEnabled": [ldap3.MODIFY_REPLACE, 'true']}
      )
    print(ldap_operation_result)

  def dn_exists(self, dn):
    print("Querying LDAP for dn {}".format(dn))
    result = self.ldap_conn.search(search_base=dn, search_filter='(objectClass=*)', search_scope=ldap3.BASE, attributes=['*'])
    if result:
        key_doc = ldif_utils.get_document_from_entry(self.ldap_conn.response[0]['dn'], self.ldap_conn.response[0]['attributes'])
        if key_doc:
            return key_doc[1]

  def import_ldif(self, ldif_files, bucket=None, force=None):
    print("Importing ldif file(s): {} ".format(', '.join(ldif_files)))

    for ldif_fn in ldif_files:
      print("Importing entries from " + ldif_fn)
      parser = ldif_utils.myLdifParser(ldif_fn)
      parser.parse()
      for dn, entry in parser.entries:
        if 'add' in  entry and 'changetype' in entry:
          print("LDAP modify add dn:{} entry:{}".format(dn, dict(entry)))
          change_attr = entry['add'][0]
          ldap_operation_result = self.ldap_conn.modify(dn, {change_attr: [(ldap3.MODIFY_ADD, entry[change_attr])]})
          print(ldap_operation_result)
        elif 'replace' in  entry and 'changetype' in entry:
          print("LDAP modify replace dn:{} entry:{}".format(dn, dict(entry)))
          change_attr = entry['replace'][0]
          ldap_operation_result = self.ldap_conn.modify(dn, {change_attr: [(ldap3.MODIFY_REPLACE, [entry[change_attr][0]])]})
          print(ldap_operation_result)
        elif not self.dn_exists(dn):
          print("Adding LDAP dn:{} entry:{}".format(dn, dict(entry)))
          ldap_operation_result = self.ldap_conn.add(dn, attributes=entry)
          print(ldap_operation_result)

  def delete_ldif(self, ldif_files, bucket=None, force=None):
    print("Deleting records, ldif file(s): {} ".format(', '.join(ldif_files)))
    
    for ldif_fn in ldif_files:
      print("Deleting entries from " + ldif_fn)
      parser = ldif_utils.myLdifParser(ldif_fn)
      parser.parse()
      for dn, _ in parser.entries:
        self.ldap_conn.delete(dn)

  def get_file_data(self, filename):
    with open(filename) as f:
      return f.read()
  
  def write_data_in_file(self, filename, filetext):
    with open(filename, 'w') as f:
      return f.write(filetext)

  def populate_file(self, filename, values, is_file_json = False):
    print("Populating file", filename)
    if is_file_json:
      # due to format function filename problem
      # https://stackoverflow.com/questions/5466451/how-can-i-print-literal-curly-brace-characters-in-a-string-and-also-use-format
      filetext = self.get_file_data(filename)
      self.write_data_in_file(filename, self.preformat(filetext))

    filetext = self.get_file_data(filename)

    self.write_data_in_file(filename, filetext.format(**values))

  def preformat(self, msg):
    """ allow {{key}} to be used for formatting in text

    that already uses curly braces.  First switch this into
    something else, replace curlies with double curlies, and then
    switch back to regular braces
    """
    msg = msg.replace('{{', '<<<').replace('}}', '>>>')
    msg = msg.replace('{', '{{').replace('}', '}}')
    msg = msg.replace('<<<', '{').replace('>>>', '}')
    return msg
  
  def get_idp_signing_cert(self, provider_host):
    makeRequest = request.Request('https://{}/idp/shibboleth'.format(provider_host))
    url = request.urlopen(makeRequest)
    xmldoc = minidom.parse(url)
    itemlist = xmldoc.getElementsByTagName('ds:X509Certificate')
    x509CertificateText = ''

    for item in itemlist:
        if item.parentNode.parentNode.parentNode.getAttribute('use') == 'signing':
            x509CertificateText =  item.firstChild.data
            break

    # remove two new line character at first
    x509CertificateText = x509CertificateText.replace('\n', '', 2)
    # replace others with space
    x509CertificateText = x509CertificateText.replace('\n', ' ')
    return x509CertificateText
