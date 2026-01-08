Feature: FlexPay

  @TC_001
  Scenario: Full flow
    Given The Customer is on Udyam registation page
    #Then Agent Verifies the Customer
    #Then Customer login to the account and completes vkyc
    Then The Customer logs in and complete esign
    #Then The Customer completes emandate
    #Then Agent performs Pendings open
    #Then Customer should have a active loan


  # @TC_002
  # Scenario: Full flow with esing -4
  #   Given The Customer is on Udyam registation page
  #   Then Agent Verifies the Customer
  #   Then Customer login to the account and completes vkyc
  #   Then The Customer logs in and complete esign with -4
  #   Then Agent performs Pendings open to confirm esign
  #   Then The Customer completes emandate
  #   Then Agent performs Pendings open
  #   Then Customer should have a active loan
  