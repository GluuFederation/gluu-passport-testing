#!/usr/bin/env bash

##############################################################################
##                                                                          ##
##     ALL TESTS ARE MADE REACHING A PRESELECTED PROVIDER                   ##
##     USERS ARE CREATED ON PROVIDER VIA API                                ##
##                                                                          ##
##############################################################################
echo "PLEASE DO NOT INTERRUPT"

## Settings down here
setup_test_env() {
    export PASSPORT_HOST=t1.techno24x7.com
    export PROVIDER_HOST=t3.techno24x7.com
    export CLIENT_HOST=chris.testingenv.org
    export API_CLIENT_ID=5aba39e9-c8fe-47de-a231-1b57efb347ab
    export API_CLIENT_SECRET=FSjEHsqDPs5vVzdlF390D4EqeYd5noZqKymLjH1W
    echo ============================================================================
    echo "Setting up environment...."
    echo PASSPORT_HOST=$PASSPORT_HOST
    echo PROVIDER_HOST=$PROVIDER_HOST
    echo CLIENT_HOST=$CLIENT_HOST
    echo API_CLIENT_ID=$API_CLIENT_ID
    echo API_CLIENT_SECRET=$API_CLIENT_SECRET
    echo ============================================================================
}

setup_test_env


export USER_NAME=johndoe22
export USER_PASSWORD=test123
export USER_MAIL=johndoe22@test.ocom
export USER_GIVEN=john
export USER_SUR=doe


# DEPENDS ON ADMIN API
function create_test_user(){
    echo "Creating test user on $PROVIDER_HOST..."
    python ./tests/helpers/create_test_user.py
}
create_test_user

# TEST 1: PASSPORT-SAML-DEFAULT
# - Provider need to be configurated manually
# - User will be created automatically

export TEST_CASE_NAME=PASSPORT-SAML-DEFAULT
export ACR=passport-saml

# PROVIDER_TYPE:
# - IDP
# - oauth provider
# - oidc provider straight
# - oidc provider oxd
export PROVIDER_TYPE=IDP

function setup_test_client() {
    # setup custom provider on test client
    echo "Setting up test client with pre-selected provider $PROVIDER_ID..."
    echo "https://$CLIENT_HOST/configuration"
    curl -k -H "Content-Type: application/json" \
    --request POST \
    --data '{"provider_id":"'$PROVIDER_ID'"}' \
    https://$CLIENT_HOST/configuration
}


# FLOWS:
# - default
# - default emailreq
# - default emaillink
# - preselected provider
export FLOW=default

# PROVIDER_ID: setup manually - api not working
# TODO: check if api works
export PROVIDER_ID=saml-default
setup_test_client

# function run_blackbox_test
# $1 TEST_CASE_NAME
# $2 PROVIDER_TYPE
# $3 ACR
# $4 FLOW
function run_blackbox_test() {
    echo ============================================================================
    echo
    echo "STARTING: $TEST_CASE_NAME"
    echo
    echo ============================================================================
    echo
    echo "- Provider type: $PROVIDER_TYPE"
    echo "- Type: $ACR"
    echo "- Flow: $FLOW"
    echo "- Passport Provider ID: $PROVIDER_ID"
    echo "TODO: Creating Trust Relation on $PROVIDER_HOST automatically"
    echo
    echo "- User data:"
    echo "USER_NAME: $USER_NAME"
    echo "USER_PASSWORD: $USER_PASSWORD"
    echo "USER_MAIL: $USER_MAIL"
    echo "USER_GIVEN: $USER_GIVEN"
    echo "USER_SUR: $USER_SUR"
    echo
    echo ----------------------------------------------------------------------------
    echo "RUNNING BLACKBOX BDT TESTS:"
    echo ----------------------------------------------------------------------------
    echo
    behave ./tests/behaver/features --include protected-content
    if [[ $FLOW == 'default emaillink' ]]
    then
        behave ./tests/behaver/features --include email-linking
    fi
    echo
    echo ----------------------------------------------------------------------------
    echo
    echo "BLACKBOX BDT TESTS FINISHED FOR TEST CASE: $TEST_CASE_NAME"
    echo ============================================================================
    #behave tests/behaver/features


}

run_blackbox_test
function delete_test_user() {
    echo "Deleting test users on $PROVIDER_HOST..."
    python ./tests/helpers/delete_test_user.py
}
delete_test_user



# TEST 2: PASSPORT-SAML-DEFAULT-EMAILREQ
# - Provider need to be configurated manually
# - User will be created automatically
export TEST_CASE_NAME=PASSPORT-SAML-DEFAULT-EMAILREQ
export ACR=passport-saml

# PROVIDER_TYPE:
# - IDP
# - oauth provider
# - oidc provider straight
# - oidc provider oxd
export PROVIDER_TYPE=IDP

# FLOWS:
# - default
# - default emailreq
# - default emaillink
# - preselected provider
export FLOW="default emailreq"


# PROVIDER_ID: setup manually - api not working
# TODO: check if api works
export PROVIDER_ID=saml-emailreq

# function run_blackbox_test
# $1 TEST_CASE_NAME
# $2 PROVIDER_TYPE
# $3 ACR
# $4 FLOW



export USER_NAME="josephdoe"
export USER_MAIL="jo-sef@test.com"

create_test_user
setup_test_client
run_blackbox_test
delete_test_user

# -----------
# TEST 3: PASSPORT-SAML-DEFAULT-EMAILLINK
# - Provider need to be configurated manually
# - User will be created automatically
export TEST_CASE_NAME=PASSPORT-SAML-DEFAULT-EMAILLINK
export ACR=passport-saml
export PROVIDER_TYPE=IDP

# FLOWS:
# - default
# - default emailreq
# - default emaillink
# - preselected provider
export FLOW="default emaillink"


# PROVIDER_ID: setup manually - api not working
# TODO: check if api works
export PROVIDER_ID=saml-email-link

# same e-mail from user josephdoe
export USER_NAME="josephdoe2"
export USER_MAIL="jo-sef@test.com"

create_test_user
setup_test_client
run_blackbox_test
delete_test_user


# -----------
# TEST 4: PASSPORT-SAML-DEFAULT-PRESELECTEDPROVIDER
# - Provider need to be configurated manually
# - User will be created automatically

export TEST_CASE_NAME=PASSPORT-SAML-DEFAULT-PRESELECTEDPROVIDER
export ACR=passport-saml
export PROVIDER_TYPE=IDP

# FLOWS:
# - default
# - default emailreq
# - default emaillink
# - preselected provider
export FLOW="preselected provider"


# PROVIDER_ID: setup manually - api not working
# TODO: check if api works
export PROVIDER_ID=saml-default

# same e-mail from user josephdoe
export USER_NAME="josephdoe2"
export USER_MAIL="jo-sef@test.com"

create_test_user
setup_test_client
run_blackbox_test
delete_test_user


echo "ALL TEST FINISHED."


echo "====================================================================="

