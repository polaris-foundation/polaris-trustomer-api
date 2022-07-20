Feature: Trustomer configuration

  Scenario: Getting the entire trustomer configuration
    Given I have trustomer headers for dev
    When I get trustomer configuration
    Then I see it matches the trustomer config file

  Scenario: Getting the entire trustomer configuration without auth
    Given I have no trustomer headers
    When I get trustomer configuration
    Then I get an error

  Scenario: Getting a specific trustomer configuration
    Given I have trustomer headers for dev
    When I get trustomer configuration for dev
    Then I see it matches the trustomer config file

  Scenario: Getting a specific trustomer configuration for a different trust
    Given I have trustomer headers for staging
    When I get trustomer configuration for dev
    Then I get an error
