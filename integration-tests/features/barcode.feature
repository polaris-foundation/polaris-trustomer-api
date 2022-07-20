Feature: Parsing patient barcodes

    Background:
        Given I have trustomer headers for dev

    Scenario Outline: Parse barcodes in various trustomer-configured formats
        When I parse patient barcode in <format> format
        Then I get the barcode information as defined by the <format>
        Examples:
        | format |
        | SWFT   | 
        | OUH    |

    Scenario: Parse invalid barcodes
        When I parse patient barcode in unsupported format
        Then I get no barcode information
