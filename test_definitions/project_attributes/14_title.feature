@iati-activity
Feature: Title

  Scenario Outline: Title is present
    Given an IATI activity
     And the activity is current
     Then `title/narrative/text()` should be present

  Scenario Outline: Title has at least 10 characters
    Given an IATI activity
     And the activity is current
     Then `title/narrative/text()` should have at least 10 characters
