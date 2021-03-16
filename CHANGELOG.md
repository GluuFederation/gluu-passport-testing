## v0.11.0 (2021-03-16)

### Feat

- add info to stdout on droplet destroy

## v0.10.0 (2020-11-28)

### Feat

- **destroy_droplets**: print droplets actions to fup w/ deleting

### Fix

- **env.sh**: Add teardown function that delete droplets on exit status != 0
- **behave**: add import sys to behaves env
- **test.conf**: delete test.conf from repo
- **.gitignore**: add test.conf to gitignore to avoid overwrite

## v0.9.2 (2020-11-26)

### Fix

- **.gitignore**: add test.conf to gitignore to avoid overwriting

## v0.9.1 (2020-10-30)

### Fix

- **test.conf**: removed comments
- **destroy_droplet.py**: fix pagination bumping pydoautomator version

## v0.9.0 (2020-10-29)

### Feat

- **create_Droplet.Py**: added tag psp-stage

## v0.8.1 (2020-10-28)

### Refactor

- **test.conf**: change default values
- **env.sh**: merging master
- **env.sh**: droplet deletion
- **env.sh**: fix changed snapshot ids
- **env.sh**: update droplet id

### Fix

- **env.sh**: remove auto-merge comments
- **env.sh**: droplet deletion if create_drplet = false

## v0.8.0 (2020-10-28)

### Fix

- **env.Sh**: fixed review changes

### Feat

- **env.Sh**: take a configuration from file

## v0.7.0 (2020-10-24)

### Fix

- **setup.properties**: fix floating ip
- **gluu.sh**: finished message on setup
- **env.sh**: getopts was expecting arg
- **create_droplet.py**: vpc_uuid cannot be null
- **create_droplet.py**: workaround to config - setting up key ids

## v0.6.0 (2020-10-20)

### Feat

- **destroy_droplet.py**: destroy droplet after test

### Fix

- **env.sh**: syntax: add ;; line 22

## v0.5.0 (2020-10-16)

### Feat

- **env.sh**: skip tests option so can be triggered by jenkins etc
- **gluu.sh**: Choose to install latest stable / latest dev
- **env.sh**: Add -s option to skipp droplet creation

### Fix

- **environment.py**: add correct behaviour for debug on error
- **environment**: Handles DEBUG_ON_ERROR and stack trace
- **env.sh**: settings
- **env.sh**: Correct boolean value of skip_droplets condition
- **passport-central-config.json**: Change issuer and add hostname jinja

### Refactor

- **create_droplet.py**: add jenkins ssh key

## v0.4.3 (2020-10-05)

### Fix

- **env.sh**: Uncomment droplet creation

## v0.4.2 (2020-10-05)

### Refactor

- **/setup/9gluu**: Fixed wrong description, no impact

### Fix

- **protected-content.py**: removed slash from getIdpInitiatedLink
- **templates**: Fix missing templates

## v0.4.0 (2020-10-04)

### Feat

- **env.sh**: Use create_droplet and server_up_chack

## v0.3.0 (2020-09-17)

### Feat

- readme updated with setup instructions
- prepare.sh also creates flag file
- added configure_client function to post to configure client api

## v0.2.1 (2020-08-12)

## v0.0.1 (2020-08-11)
