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
    And current date is "2015-02-15"
    When I run "./oneliner test line"
    Then a file named "some_dir/2015-02-15.txt" should exist
    And the file "some_dir/2015-02-15.txt" should contain:
    """
    test line
    """
