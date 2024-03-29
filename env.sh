#!/usr/bin/env bash

##############################################################################
##                                                                          ##
##     ALL TESTS ARE MADE REACHING A PRESELECTED PROVIDER                   ##
##     USERS ARE CREATED ON PROVIDER VIA API                                ##
##                                                                          ##
##############################################################################

# Default value: true
create_drplet=true;
run_tests=true;

## CLI options
# -s skip droplets creation automation (tests only)
# -t skip tests
# -c <file> : to load config from file

while getopts ":stc:" option; do
   case $option in
      s) create_drplet=false;;
      t) run_tests=false;;
      c)
        config_file=${OPTARG}
        if [ ! -s ${config_file} ];
        then
            echo "Configuration file not found. Pass it using './enc.sh -c <file>' option or skip '-c' option to take config from 'test.conf'"
            exit
        fi
        ;;
     \?) # incorrect option
         echo "Error: Invalid option"
         exit;;
   esac
done

# geckodriver
export PATH=$PATH:$PWD/tests/selenium/drivers/firefox


# SETUP OD_TOKEN (digital ocean token b4 stating)
echo "PLEASE DO NOT INTERRUPT"

teardown() {
    exit_status=$(echo "$?")
    echo "entered teardown..."
    echo "EXIT detected with exit status $exit_status"
    if [[ $exit_status != 0 ]]
    then
        echo "Fetching artifacts from teardown..."
        fetch_artifacts
        echo "Deleting droplets..."
        delete_droplets
    fi
}

# exit when any command fails
set -e
trap 'teardown' EXIT


## Settings down here
setup_test_env() {
    echo ============================================================================
    if [ -z ${config_file} ];
    then
        config_file="test.conf"
    fi
    echo "Configuration is loading from $config_file file"
    . $config_file
    export $(cut -d= -f1 $config_file)

    echo ============================================================================
    echo "Setting up environment...."
    echo PASSPORT_HOST=$PASSPORT_HOST
    echo PASSPORT_IP=$PASSPORT_IP
    echo PROVIDER_HOST=$PROVIDER_HOST
    echo PROVIDER_IP=$PROVIDER_IP
    echo PROVIDER_SNAPSHOT_ID=$PROVIDER_SNAPSHOT_ID
    echo CLIENT_HOST=$CLIENT_HOST
    echo API_CLIENT_ID=$API_CLIENT_ID
    echo API_CLIENT_SECRET=$API_CLIENT_SECRET
    echo LATEST_DEV_SNAPSHOT_ID=$LATEST_DEV_SNAPSHOT_ID
    echo LATEST_STABLE_SNAPSHOT_ID=$LATEST_STABLE_SNAPSHOT_ID
    echo ============================================================================

}


setup_test_env
fetch_artifacts() {
    echo "cleaning up old artifacts"
    rm -r server_artifacts

    mkdir -p server_artifacts/passport
    echo "Fetching logs from passport server $PASSPORT_HOST"
    scp -r -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@"$PASSPORT_HOST":/opt/gluu-server/opt/gluu/jetty/oxauth/logs/*.log ./server_artifacts/passport/.
    scp -r -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@"$PASSPORT_HOST":/opt/gluu-server/opt/gluu/jetty/identity/logs/*.log ./server_artifacts/passport/.
    scp -r -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@"$PASSPORT_HOST":/opt/gluu-server/opt/gluu/node/passport/logs/*.log ./server_artifacts/passport/.

    mkdir -p server_artifacts/provider
    echo "Fetching logs from passport server $PROVIDER_HOST"
    scp -r -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@"$PROVIDER_HOST":/opt/gluu-server/opt/gluu/jetty/oxauth/logs/*.log ./server_artifacts/provider/.
    scp -r -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@"$PROVIDER_HOST":/opt/gluu-server/opt/gluu/jetty/identity/logs/*.log ./server_artifacts/provider/.
    scp -r -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@"$PROVIDER_HOST":/opt/gluu-server/opt/shibboleth-idp/logs/*.log ./server_artifacts/provider/.
}

delete_droplets() {

    delete_passport_droplet(){
        export DROPLET_HOST=$PASSPORT_HOST
        python ./tests/helpers/destroy_droplet.py
        export DROPLET_HOST=
    }

    delete_provider_droplet(){
        export DROPLET_HOST=$PROVIDER_HOST
        python ./tests/helpers/destroy_droplet.py
        export DROPLET_HOST
    }
    delete_provider_droplet
    delete_passport_droplet

}
create_droplets() {

    echo 'Creating droplets...'

    ## creates passport droplet and wait till is up (takes a while)
    create_passport_droplet(){
        export DROPLET_HOST=$PASSPORT_HOST
        export FLOATING_IP=$PASSPORT_IP
        export SNAPSHOT_ID=$LATEST_STABLE_SNAPSHOT_ID
        python ./tests/helpers/create_droplet.py
        export DROPLET_HOST=
        export FLOATING_IP=
        export SNAPSHOT_ID=
    }



    create_provider_droplet(){
        export DROPLET_HOST=$PROVIDER_HOST
        export FLOATING_IP=$PROVIDER_IP
        export SNAPSHOT_ID=$PROVIDER_SNAPSHOT_ID
        python ./tests/helpers/create_droplet.py
        export DROPLET_HOST=
        export FLOATING_IP=
        export SNAPSHOT_ID=
    }




    wait_till_server_up(){
        export SERVER=$1
        python ./tests/helpers/server_up_check.py
        export SERVER=
    }

    create_passport_droplet
    wait_till_server_up $PASSPORT_HOST
    create_provider_droplet
    wait_till_server_up $PROVIDER_HOST
    wait_till_server_up "${PROVIDER_HOST}/idp/shibboleth"
    echo "Yeah well, looks like they're up!"

    # Is not possible to set / force metadata retrieve in shibboleth
    echo "Waiting 5 minutes till IDP fetches SPs metadata..."
    sleep 5m

}

### Calls register and configuration endpoint to register and setup client/secret at auth-tdd-client
configure_client() {
    register_client=$(curl -k -X POST 'https://'$CLIENT_HOST'/register' -H 'Content-Type: application/json' --data-raw '{
    "op_url": "https://'$PASSPORT_HOST'",
    "client_url": "https://'$CLIENT_HOST'"
    }')

    curl -k -X POST 'https://'$CLIENT_HOST'/configuration' \
    -H 'Content-Type: application/json' --data-raw "$register_client"
}

# DEPENDS ON ADMIN API
function create_test_user(){
    echo "Creating test user on $PROVIDER_HOST..."
    python ./tests/helpers/create_test_user.py
}

function delete_test_user() {
    echo "Deleting test users on $PROVIDER_HOST..."
    python ./tests/helpers/delete_test_user.py
}

function setup_test_client() {
    # setup custom provider on test client
    echo "Setting up test client with pre-selected provider $PROVIDER_ID..."
    echo "https://$CLIENT_HOST/configuration"
    curl -k -H "Content-Type: application/json" \
    --request POST \
    --data '{"provider_id":"'$PROVIDER_ID'"}' \
    https://$CLIENT_HOST/configuration
}

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
    # if [[ $FLOW == 'default emaillink' ]]
    # then
    #     behave ./tests/behaver/features --include email-linking
    # fi
    echo
    echo ----------------------------------------------------------------------------
    echo
    echo "BLACKBOX BDT TESTS FINISHED FOR TEST CASE: $TEST_CASE_NAME"
    echo ============================================================================
}

run_all_tests(){
    configure_client

    export USER_NAME=johndoe22
    export USER_PASSWORD=test123
    export USER_MAIL=johndoe22@test.ocom
    export USER_GIVEN=john
    export USER_SUR=doe

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

    # FLOWS:
    # - default
    # - default emailreq
    # - default emaillink
    # - preselected provider
    # - idp-initiated
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


    run_blackbox_test

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
    export PROVIDER_ID=saml-emaillink

    # same e-mail from user josephdoe
    export USER_NAME="josephdoe2"
    export USER_MAIL="jo-sef@test.com"

    create_test_user
    setup_test_client
    run_blackbox_test
    delete_test_user



    # TEST 4: PASSPORT-SAML-IDP-INITIATED
    # - Provider need to be configurated manually
    # - User will be created automatically
    export TEST_CASE_NAME=PASSPORT-SAML-IDP-INITIATED
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
    # - idp-initiated
    export FLOW="idp-initiated"


    # PROVIDER_ID: setup manually - api not working
    # TODO: check if api works
    export PROVIDER_ID=saml-idpinit


    export USER_NAME=hansdoe
    export USER_MAIL="hansdoe@test.com"
    export USER_GIVEN=hans
    export USER_SUR=doe

    create_test_user
    setup_test_client
    run_blackbox_test
    delete_test_user

    echo "ALL TEST FINISHED."

    echo "====================================================================="
}


echo "create_drplet=$create_drplet"
echo "run_tests=$run_tests"

if [ "$create_drplet" = true ] ; then
    create_droplets
fi

if [ "$run_tests" = true ] ; then
    run_all_tests
fi

# Try to delete droplet after tests
if [ "$create_drplet" = false ] ; then
    echo "Fetching artifacts from teardown..."
    fetch_artifacts
    echo "Deleting droplets..."
    delete_droplets
    echo "finished with success!!!"
fi


