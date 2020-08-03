# Gluu-Passport Blackbox Testing

## Goal

- Automate all the passport flows

## Sumary

I was trying to setup automatically: 
- Gluu to act as IDP / OP
- Gluu running passport
- Client app

Tried some different approachs, I would like to build - test - destroy docker. But to have **system.d** running inside containers is not much recommended (except for CI testing, but even like that, would involve editing postinstall script and doing it automatically can be messy).

So after discarding some options, I came to this approach:

- Snapshot containing IDP / OP 
- Snapshot containing LDIF testing data
- Snapshot containing client app

So basically, what to do now is:

- script to automate droplet creation from snapshots
- script to install last build and import LDIF testing data
- run passport integration tests
- script to destroy droplets

## What to do

- Setup OP/IDP server
- Install latest version - Connect to external database
- Create tests users on idp/op server **automated**
- Setup test client **done**


### Automated Login Flows

- SAML default
- SAML email requiring
- SAML email linking


### Setup should be done on env.sh file
