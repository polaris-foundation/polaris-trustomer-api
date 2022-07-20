Feature: Escalation policy

    Background:
        Given I have trustomer headers for dev

    Scenario: Getting valid escalation policy
        When I get news2 escalation policy
        Then I see it contains the following configuration options
            | name                  | value                              |
            | routine_monitoring    | <p>Continue routine monitoring</p> |
            | low_monitoring        | <p>Low monitoring policy here</p>  | 
            | low_medium_monitoring | <p>Low to medium policy</p>        | 
            | medium_monitoring     | <p>Medium monitoring policy</p>    |
            | high_monitoring       | <p>High monitoring policy</p>      |

    Scenario: Getting empty escalation policy
        When I get my_policy escalation policy
        Then I see it contains no configuration options

    Scenario: Getting non-existent escalation policy
        When I get non-existent escalation policy
        Then I see it contains no configuration options
