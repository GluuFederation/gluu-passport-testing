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
