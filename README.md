# Gluu-Passport Blackbox Testing

## Goal

- Automate tests for all the passport flows

## How we do it

Creating a **stage** environment like:

![How we do it](./docs/resources/passport_integration_tests.png)

## What to do

- Setup OP/IDP server
- Install latest version - Connect to external database
- Create tests users on idp/op server **automated**
- Setup test client **done**

### Automated Login Flows

- SAML default
- SAML email requiring
- SAML email linking
- [ ] OIDC

### Setup should be done on env.sh file

## TO BE

### In the near future

This is a nice milestone...

![TO BE](./docs/resources/passport_integration_tests-TO-BE.png)