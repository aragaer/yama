Feature: Deploy on Heroku
  As a Oneliner developer
  I want my application to run on Heroku
  So that I do not worry much about my own hosting

  Scenario: Starting in foreman
    Given I use the project directory as working directory
    When I run "foreman start" in background
    And I wait for 1 second
    And I run "curl localhost:5000"
    Then it should pass with:
    """
    Hello, world
    """

  Scenario: Using environment variables
    Given I use the project directory as working directory
    And I set the environment variable "PORT" to "5050"
    When I run "foreman start" in background
    And I wait for 1 second
    And I run "curl localhost:5050"
    Then it should pass with:
    """
    Hello, world
    """
