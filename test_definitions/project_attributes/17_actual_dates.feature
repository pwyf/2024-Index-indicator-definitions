@iati-activity
Feature: Actual dates

  Scenario Outline: Actual start date is present
    Given an IATI activity
     And the activity is current
     And `activity-status/@code` is one of 2, 3 or 4
     Then `activity-date[@type="2"]` should be present

  Scenario Outline: Actual end date is present
    Given an IATI activity
     And the activity is current
     And `activity-status/@code` is one of 3 or 4
     Then `activity-date[@type="4"]` should be present
