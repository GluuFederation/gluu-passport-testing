#!/usr/bin/env bash

##############################################################################
##                                                                          ##
##     THIS TEST CASES USES THE TEST SERVER's GLUU CE                       ##
##                                                                          ##
##############################################################################

# setup Gluu Stable version
install_gluu_ce() {
    ## This commands need sudo permission
    ### Ads and install latest STABLE package for ubuntu 18
    echo "deb https://repo.gluu.org/ubuntu/ bionic main" > /etc/apt/sources.list.d/gluu-repo.list

    sudo curl https://repo.gluu.org/ubuntu/gluu-apt.key | apt-key add -
    sudo apt update -y
    sudo apt install gluu-server -y
    sudo apt-mark hold gluu-server
    
    ### copy setup files to chmod
    echo "Copying setup.properties file to chmod..."
    sudo cp $WORKSPACE/setup.properties /opt/gluu-server/install/community-edition-setup/
    
    ssh -o IdentityFile=/etc/gluu/keys/gluu-console -o Port=60022 -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null -o PubkeyAuthentication=yes root@localhost "cd /install/community-edition-setup && ./setup.py"
}

# geckodriver
export PATH=$PATH:$PWD/tests/selenium/drivers/firefox


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

function run_config_fetch_blackbox_test() {
    # this test uses gluu server which is on testing server(the server where we deploy this tests)
    echo ----------------------------------------------------------------------------
    echo "RUNNING CONFIG FETCH BLACKBOX BDT TESTS:"
    echo ----------------------------------------------------------------------------
    export PASSPORT_LOG_FILE='/opt/gluu-server/opt/gluu/node/passport/logs/passport.log'
    export TEST_SERVER_HOST=$TEST_SERVER_HOST

    echo "PASSPORT_LOG_FILE: $PASSPORT_LOG_FILE"
    echo "TEST_SERVER_HOST: $TEST_SERVER_HOST"

    behave ./tests/behaver/features --include fetch-config
}

run_all_tests(){
    run_config_fetch_blackbox_test
    echo "ALL TEST FINISHED."
    echo "====================================================================="
}
run_all_tests
