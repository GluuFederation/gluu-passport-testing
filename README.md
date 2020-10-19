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

## Setup

### Setting up passport droplet

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

### Setup should be done on env.sh file, please check it

## Starting test server

Just restart and see the magic happening on `/test-data/gluu.log`
```sh
shutdown -r
```

#### Configyration should be done on env.sh file, please check it


### Setting up test suite

Install Xvfb
`sudo apt install xvfb`

Add geckodriver to your path:
`export PATH=$PATH:$PWD/tests/selenium/drivers/firefox`

In your project root folder, create a virtual env using:
`python3 -m venv venv`

Enter the venv:
`source venv/bin/activate`

Install poetry if you don't have:
`curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`

Install dependencies:
`poetry install`

If you don't have, install Firefox:
`apt install firefox`

Setup ENV on `env.sh` file

run `env.sh`

### Options
You can run `env.sh` with skip options:
- `-s`: skip droplet creation
- `-t`: skip tests

## TO BE

### In the near future

This is a nice milestone...

![TO BE](./docs/resources/passport_integration_tests-TO-BE.png)