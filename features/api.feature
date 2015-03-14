Feature: Simple api
  As a forgetful person
  I want to have a web API for my memos
  So that I could choose between multiple available clients to write and read my memos

  Background: Clean database
    Given I have empty database

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

  Scenario: Writing a line
    Given the date is '2015-03-10'
    When I post to '/memos/daily' the following text:
    """
    Just a test line here
    """
    Then I have the following memos for date 2015-03-10:
    """
    Just a test line here
    """

  Scenario: Today lines
    Given the date is '2015-03-14'
    And I have the following memos for date 2015-03-14:
    """
    Test line
    Another test line
    """
    When I access the resource '/memos/daily/today'
    Then I get the following list of memos:
    """
    Test line
    Another test line
    """
