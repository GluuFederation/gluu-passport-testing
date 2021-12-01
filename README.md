# Gluu-Passport Blackbox Testing

## Goal

- Automate tests for all the passport flows

## How we do it

Creating a **stage** environment like:

![How we do it](./docs/resources/passport_integration_tests.png)

## Snapshot setup

### 1. Passport Host Setup

Passport Host not need any extra setup. It is just need fresh UB 20 snapshot. During test case run, It install Gluu CE in it, install Data and perform test.

### 2. Provider Host Setup

Provider host need snapshot with Gluu CE IDP 4.3.0. During test case run, It install data, add TR and setup SP metadata.

## ENV.sh Steps

[env.sh](env.sh) is the use to handle whole test flow. It used to configure, setup server and run test cases. 

### Configuration

- Setup 
  - Install Xvfb `sudo apt install xvfb`
  
  - Install `poetry` if you don't have: curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
  
  - Install dependencies: `poetry install`
  
  - If you don't have, install Firefox: `apt install firefox`

  - Install Python LDAP3 for DB Operations: `pip install ldap3`

- Configuration

    - Use `test.conf` for configuration. You can pass any file by using option `-c <file>`.

    - Configuration details are as given below:

    | Env | Description |
    |-----|-------------|
    |**PASSPORT_HOST**|Use to set Host for Passport Droplet|
    |**PASSPORT_IP**|Use to set floating IP for Passport Droplet|
    |**LATEST_DEV_SNAPSHOT_ID**|It is `Dev Passport Snapshot Id` from which you want to create droplet for Passport|
    |**LATEST_STABLE_SNAPSHOT_ID**|It is `Stable Passport Snapshot Id` from which you want to create droplet for Passport|
    |**PROVIDER_HOST**|Use to set Host for SAML IDP Provider Droplet|
    |**PROVIDER_IP**|Use to set floating IP for SAML IDP Provider Droplet|
    |**PROVIDER_SNAPSHOT_ID**|It is `SAML IDP Provider Snapshot Id` from which you want to create droplet for SAML IDP Provider|
    |**CLIENT_HOST**|It is use to set Host for Request Party Client i.e. [auth-tdd-client](https://github.com/christian-hawk/auth-tdd-client)|
    |**GLUU_VERSION**|Two values allow here `LATEST-STABLE` or `LATEST-DEV`. As per version, Gluu CE version installed on PASSPORT Host.|

    - Example of test.conf:
    ```
    PASSPORT_HOST=test.yourpassport.com
    PASSPORT_IP="100.xx.xx.xx"
    LATEST_DEV_SNAPSHOT_ID=xxxxxx
    LATEST_STABLE_SNAPSHOT_ID=xxxxxx
    PROVIDER_HOST=test.youridphost.com
    PROVIDER_IP="101.xx.x.x"
    PROVIDER_SNAPSHOT_ID=xxxxx
    CLIENT_HOST=xxx.xxx.com
    TEST_SERVER_HOST=xxx.xxx.com
    GLUU_VERSION=LATEST-STABLE
    ```

- Options

    - Options available in `env.sh` to handle different task.

    - Example: `./env.sh -[option]`

    | Option | Description |
    |--------|-------------|
    | -c | Use to create the droplets |
    | -t | Use to run test cases |
    | -s | Use to install and setup Gluu on Passport Host and add data on Passport and IDP Host |
    | -l | Use to fetch artifacts logs files |
    | -d | Use to delete the droplets |

### Create Droplet

`-c` option is use to create droplet.

```
./env.sh -c
```

### Setup PASSPORT and PROVIDER HOST

`-s` option is use to setup PASSPORT and PROVIDER Host. In this stage, It insert test data into directly ldap db on passport host and provider host.

```
./env.sh -s
```

Its perform tasks:

- Install latest Gluu on PASSPORT Host
    
    In this stage, env.sh helps to connect PASSPORT Host and install Gluu CE using install.sh

    In install.sh, we are using `setup.properties` which helps to pass preconfigured setup values.
    
- Manage Data on PASSPORT and Provider Host

    In this stage, env.sh helps to insert, remove and update data in ldap using `python-ldap3` module to connect db and perform CRUD operation.
    
    Checkout passport_host_data.py, passport_host_data.py, and ldifs in data folder for examples and implementation.
