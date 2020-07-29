Feature: accessing protected content

    Scenario: Not authenticated user access protected content
        Given that user exists in provider
        When user tries to access protected content page
        Then user should be redirected to login page


    Scenario: Authenticated user access protected content
        Given that user exists in provider
            And user is authenticated
        When user tries to access protected content page
        Then user should access protected content

