from ldaphelper import Passport
import json

# creating providers
passport = Passport('cn=directory manager','Test123$')

#print(passport.gpc_providers())

f = open('tests/providers.json')

read = f.read()
js = json.loads(read)
providers = js['providers']


f.close()
for provider in providers:
    passport.add_provider(**provider)