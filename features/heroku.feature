Feature: Deploy on Heroku
  As a Oneliner developer
  I want my application to run on Heroku
  So that I do not worry much about my own hosting

  Background: Working directory
    Given I use the project directory as working directory

  Scenario: Starting in foreman
    When I run "foreman start" in background
    And I wait for 1 second
    And I run "curl localhost:5000"
    Then it should pass with:
    """
    Hello, world
    """

  Scenario: Using environment variables
    Given I set the environment variable "PORT" to "5050"
    When I run "foreman start" in background
    And I wait for 1 second
    And I run "curl localhost:5050"
    Then it should pass with:
    """
    Hello, world
    """

  Scenario: Write and read:
    And I set the environment variable "PORT" to "5052"
    When I run "foreman start" in background
    And I wait for 1 second
    And I run "curl localhost:5052/memos/daily -d 'test message'"
    And I run "curl localhost:5052/memos/daily/today"
    Then it should pass with:
    """
    ["test message"]
    """

  Scenario: Using actual mongodb
    Given I set the environment variable "MONGO_URL" to "mongodb://localhost:27017/one-liner"
    And I set the environment variable "PORT" to "5051"
    And I create an empty oneliner database at "mongodb://localhost:27017/one-liner"
    And I have the following memos for today:
    """
    Test line
    Another test line
    """
    When I run "foreman start" in background
    And I wait for 1 second
    And I run "curl localhost:5051/memos/daily/today"
    Then it should pass with:
    """
    ["Test line", "Another test line"]
    """
