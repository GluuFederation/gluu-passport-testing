from ldaphelper import Op, LdapConnector
import json
from flask_oidc import registration, discovery
import os


disc = discovery.discover_OP_information('https://chris.gluutwo.org')

reg = registration.register_client(disc,['https://chris.gluuthree.org/callback'])
