@iati-activity
Feature: Commitment

  Scenario Outline: Commitment is present
    Given an IATI activity
     And the activity is current
     And `activity-status/@code` is one of 2, 3 or 4
     Then `transaction[transaction-type/@code="2"]` should be present and of non-zero value
