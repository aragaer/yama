Feature: Command-line scratchpad writer
  As a forgetful person
  I want to be able to write lines of text to a files
  So that I could later read the text I wrote

  Scenario: Running the application
    Given a new working directory
    And a file named "oneliner.config" with:
    """
    path = ./some_dir
    """
    And a directory named "some_dir"
    When I run "oneliner test line"
    Then a file for today date should exist in "some_dir" with:
    """
    test line
    """
