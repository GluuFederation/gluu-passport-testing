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

### Configyration should be done on env.sh file, please check it

## TO BE

### In the near future

This is a nice milestone...

![TO BE](./docs/resources/passport_integration_tests-TO-BE.png)