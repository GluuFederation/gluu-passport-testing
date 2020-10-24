# Gluu-Passport Blackbox Testing

## Goal

- Automate tests for all the passport flows

## How we do it

Creating a **stage** environment like:

![How we do it](./docs/resources/passport_integration_tests.png)

## Starting

Clone this reppo to your test server / CI server

## Setup

### Setting up provider (idp/op) droplet
`@TODO`

### Setting up passport droplet

- Setup your SP static IP (you need a static ip reserved, preffered a `floating_ip`) and host name
    - In the project root:
        ```
        vim setup/setup.properties
        ```
    - Locate the line with `ip=`
    - Update with the static IP address
    - Locate the line with `hostname=`
    - Update with your passport hostname
- Edit `setup/templates/passport-central-config.json` to configure your passport SPs
- In case you want certificates (recommended):
    - run:
        ```
        certbot --apache --agree-tos --force-renewal -m your@realemail.org -n -d <passporthost>
        ```
        (replace passporthost for your passport host, i.e. `test.gluu.org`)
    - compress `etc/letsecrypt`
        ```
        tar -czvf etcletsencrypt.tar /etc/letsencrypt
        ```
        (so you will have `etcletsencrypt.tar` in your `setup` folder)


- On a fresh droplet, create folder `test-install-data`:
``` sh
ssh <yourhost> mkdir /test-install-data
```

- Copy files from setup folder to `test-install-data` that you just created on your fresh droplet:

```sh
scp -r ./setup/* <your-host>:/test-install-data/.
```

- Login to your droplet and run the `prepare.sh` file:
```sh
cd /
chmod -R 755 test-install-data
cd /test-install/data
./prepare.sh
```

- Check if flag file `freshsnap` was created:

```sh
ls /root
```


## Starting test server

Just restart (`shutdown -r`) and gluu-server will be installed w/ testing-data. Follow it on `/test-data/gluu.log`


#### Configyration should be done on env.sh file, please check it


### Setting up test suite

Install Xvfb
`sudo apt install xvfb`

Install poetry if you don't have:
`curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`

Install dependencies:
`poetry install`

If you don't have, install Firefox:
`apt install firefox`

Setup ENV on `env.sh` file

run `poetry run env.sh`

### Options
You can run `env.sh` with skip options:
- `-s`: skip droplet creation
- `-t`: skip tests

## TO BE

### In the near future

This is a nice milestone...

![TO BE](./docs/resources/passport_integration_tests-TO-BE.png)