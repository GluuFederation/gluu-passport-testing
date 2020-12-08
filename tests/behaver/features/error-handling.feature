Feature: Error Handler

    Scenario: User deny consent
        Given user never authenticated before
            And user started inbound authentication flow
        When user deny consent
        Then user should be redirected to the login page
