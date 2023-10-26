@iati-activity
Feature: Aid type

  Scenario Outline: Aid type is present
    Given an IATI activity
     And the activity is current
     And `activity-status/@code` is one of 2, 3 or 4
     Then `default-aid-type | transaction/aid-type` should be present

  Scenario Outline: Aid type is valid
    Given an IATI activity
     And the activity is current
     And `activity-status/@code` is one of 2, 3 or 4
     Then every `default-aid-type[not(@vocabulary) or @vocabulary="1"]/@code | transaction/aid-type[not(@vocabulary) or @vocabulary="1"]/@code` should be on the AidType codelist
