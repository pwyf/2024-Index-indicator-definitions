@iati-activity
Feature: Budget Alignment

  Scenario Outline: Capital spend is present
    Given an IATI activity
     And the activity is current
     And `activity-status/@code` is one of 2, 3 or 4
     And `default-aid-type/@code` is not any of A01, A02 or G01
     And `transaction/aid-type/@code` is not any of A01 or A02
     Then `capital-spend` should be present

  Scenario Outline: Publish detailed CRS purpose codes in the sector field
    Given an IATI activity
     And the activity is current
     And `activity-status/@code` is one of 2, 3 or 4
     And `default-aid-type/@code` is not any of A01, A02 or G01
     And `transaction/aid-type/@code` is not any of A01 or A02
     Then `sector/@code` should be present, or `sector/@code` should be present for every `transaction`
     And at least one `sector[not(@vocabulary) or @vocabulary="1"]/@code`, or at least one `sector[not(@vocabulary) or @vocabulary="1"]/@code` for every `transaction`, should be on the Sector codelist
     And `sector[not(@vocabulary) or @vocabulary="1"]/@code | transaction/sector[not(@vocabulary) or @vocabulary="1"]/@code` is not any of 43010, 43050, 43081, 43082, 52010, 99810, 15110, 15111, 15112, 15114, 15130, 16010, 16061, 21010, 21020, 22010, 23110, 43030 or 43040
