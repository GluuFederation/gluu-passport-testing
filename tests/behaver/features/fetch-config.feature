Feature: Fetch Configuration
    Get full configuration from oxauth

    Scenario: Successful get configuration
        Given passport is not running
            And oxauth is running
        When passport is started
            And wait for the fetch configuration time
        Then configuration should be correctly fetched
