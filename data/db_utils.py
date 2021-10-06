import ldap3
import os
import argparse
import ldif_utils

class DBUtils:

  def __init__(self):
    self.ldap_hostname = os.environ.get('LDAP_HOSTNAME') or 'localhost' 
    self.ldaps_port = os.environ.get('LDAP_PORT') or '1636'
    self.ldap_pass = os.environ.get('LDAP_PASS') or os.environ.get('PASSPORT_HOST_GLUU_ADMIN_PASSWORD')
    self.ldap_binddn = 'cn=directory manager'
    self.passport_host = os.environ.get('PASSPORT_HOST')
    self.idp_host = os.environ.get('IDP_HOST')

  def bind(self, use_ssl=True, force=False):
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
    self.log_ldap_result(ldap_operation_result)

  def import_ldif(self, ldif_files, bucket=None, force=None):
    print("Importing ldif file(s): {} ".format(', '.join(ldif_files)))
    
    for ldif_fn in ldif_files:
      print("Importing entries from " + ldif_fn)
      parser = ldif_utils.myLdifParser(ldif_fn)
      parser.parse()
      for dn, entry in parser.entries:
        backend_location = force if force else self.get_backend_location_for_dn(dn)
        if 'add' in  entry and 'changetype' in entry:
          print("LDAP modify add dn:{} entry:{}".format(dn, dict(entry)))
          change_attr = entry['add'][0]
          ldap_operation_result = self.ldap_conn.modify(dn, {change_attr: [(ldap3.MODIFY_ADD, entry[change_attr])]})
          self.log_ldap_result(ldap_operation_result)
        elif 'replace' in  entry and 'changetype' in entry:
          print("LDAP modify replace dn:{} entry:{}".format(dn, dict(entry)))
          change_attr = entry['replace'][0]
          ldap_operation_result = self.ldap_conn.modify(dn, {change_attr: [(ldap3.MODIFY_REPLACE, [entry[change_attr][0]])]})
          self.log_ldap_result(ldap_operation_result)
        elif not self.dn_exists(dn):
          print("Adding LDAP dn:{} entry:{}".format(dn, dict(entry)))
          ldap_operation_result = self.ldap_conn.add(dn, attributes=entry)
          self.log_ldap_result(ldap_operation_result)

  def delete_ldif(self, ldif_files, bucket=None, force=None):
    print("Deleting records, ldif file(s): {} ".format(', '.join(ldif_files)))
    
    for ldif_fn in ldif_files:
      print("Deleting entries from " + ldif_fn)
      parser = ldif_utils.myLdifParser(ldif_fn)
      parser.parse()
      for dn, entry in parser.entries:
        self.ldap_conn.delete(dn)


  def populate_file(self, filename, values):
    print("Populating file", filename)
    readf = open(filename)
    file_text = readf.read()
    readf.close()

    newf = open(filename, 'w')
    newf.write(file_text.format(**(values or self.__dict__)))

  def build_passport_ldif(self, passport_config_file, passport_ldif_file):
    self.populate_file(passport_config_file)

    passport_file = open(passport_config_file)
    passport_file_text = passport_file.read()
    passport_file.close()

    self.gluu_passport_configuration = passport_file_text.replace('\n', '')
    self.populate_file(passport_ldif_file)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "action", help="the action you want to perform.",
    choices=["import", "update", "delete", "populate"])
  parser.add_argument(
    "--filename", help="accept the the file with path")
  parser.add_argument(
    "--enable-script", help="accept inum to update the Personal and Custom script")

  args = parser.parse_args()
  dbUtils = DBUtils()
  dbUtils.bind()

  if args.action == 'import':
    print('Importing', args['filename'])
    dbUtils.enable_script(args['filename'])

  if args.action == 'update':
    scriptInum = args.get('enable-script')
    if scriptInum:
      dbUtils.enable_script(scriptInum)

  if args.action == 'delete':
    print('Deleting entries from', args['filename'])
    filename = args.get('filename')
    if filename:
      dbUtils.delete_ldif(filename)

  if args.action == 'populate':
    print('Populating...')
    filename = args.get('filename')
    if filename:
      dbUtils.populate_file(filename)