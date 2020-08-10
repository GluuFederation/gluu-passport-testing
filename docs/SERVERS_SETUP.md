## [t1] Setting up test server (Passport)

- Install latest gluu version

## [t3] Setting up test server (IDP/OP)

- Install 4.1 stable on ubuntu digital ocean
- IP address: DO floating
- hostname: t3
- self-signed data
- max ram 3072
- password: Test123$

### [t3] Create OP client for passport

- `oidc-register https://t3.techno24x7.com https://t1.techno24x7.com --output-file t3t1.json`

*oidc-register is part of Flask-OIDC module

### [t1] Create OIDC Passport Provider

- t3-oidc-test

### [t3] Add callback url to OP


### [t1] Create IDP Passport Provider

(SkipRequestCompression = True)

- saml-default ·─ · urn:test:default
- saml-emaillink - urn:test:link - act email linking
- saml-emailreq - urn:test:mailreq - activate e-mail req 
- saml-idpinit - chris.testingenv.org (has to contain host from url that host will be redirected) - validateInResponseTo: False

### [t3] Create IDP TR

- saml-default
- saml-emaillink - activate e-mail linking
- saml-emailreq - Don't release e-mail
- saml-idpinit

### Configure IDP Initiated Flow

- Add
- Select provider: saml-idpinit

### [t3] Enable API
- Follow documentation https://gluu.org/docs/gluu-server/4.1/api-guide/oxtrust-api (test mode)

### Setup /env.sh

### [t1] Enable pre-selected provider
- Follow documentation https://gluu.org/docs/gluu-server/4.2/authn-guide/passport/#preselecting-an-external-provider

### [t1] Select all ACRS on social and saml person scripts

### [t3] Activate basic script for authentication method
- Custom Scripts -> Basic -> All ACRS -> Enabled

### [t3] Create test users [AUTOMATED]

