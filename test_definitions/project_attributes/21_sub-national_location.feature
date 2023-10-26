@iati-activity
Feature: Sub-national location

  Scenario Outline: Location (sub-national)
    Given an IATI activity
     And the activity is current
     # The exclusion on the next line will only apply for some organisations
     And `activity-scope/@code` is not any of 1, 2, 3 or 4
     And `activity-status/@code` is one of 2, 3 or 4
     And `recipient-region/@code` is not 998
     And `default-aid-type/@code` is not any of B01, B02, F01, H01, H02, H03, H04, H05 or G01
     And `transaction/aid-type/@code` is not any of B01, B02, F01, H01, H02, H03, H04, H05 or G01
     Then `location` should be present

  Scenario Outline: Location (sub-national) point or administrative or location-id
    Given an IATI activity
     And the activity is current
     # The exclusion on the next line will only apply for some organisations
     And `activity-scope/@code` is not any of 1, 2, 3 or 4
     And `activity-status/@code` is one of 2, 3 or 4
     And `recipient-region/@code` is not 998
     And `default-aid-type/@code` is not any of B01, B02, F01, H01, H02, H03, H04, H05 or G01
     And `transaction/aid-type/@code` is not any of B01, B02, F01, H01, H02, H03, H04, H05 or G01
     Then `location/point` should be present, or at least one `location/administrative/@vocabulary | location/location-id/@vocabulary` should be on the GeographicVocabulary codelist
