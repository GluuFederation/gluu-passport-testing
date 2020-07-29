Feature: e-mail linking
    Me as a gluu customer
    Want to have users authentication methods linked by email
    To keep my information organized


    Scenario: Linking e-mail after first authentication on second provider
        Given user already authenticated with another provider
            And user has email attribute
        When user authenticates
        Then user profile should have both authentication methods
