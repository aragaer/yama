Feature: Simple api
  As a forgetful person
  I want to have a web API for my memos
  So that I could choose between multiple available clients to write and read my memos

  @skip
  Scenario: Reading the lines
    Given I have the following memos for date 2015-02-27:
    """
    Test line
    Another test line
    """
    When I access the resource '/memos/daily/2015-02-27'
    Then I get the following list of memos:
    """
    Test line
    Another test line
    """

