# Created by stn at 2018/10/20
Feature: add_new_user page and enter eshopping function

  Scenario: Login Success
    Given a user visits the site
    When a user visits the login page
    And she logs in with username "admin" and password "default"
    Then she should see a message of login success

  Scenario:  create uesr page
    When she logs in and clicks My Lists
    Then she would see a add button and click it
    And she will enter the add user page
    And she write detail with Email "Stn131415@gmail.com" and Firstname "Tianning" and Lastname "Sun" and gender "M" and Address "23 MORWICK ST" and Postcode with "2135" and city "Sydney" and Phone namber "04123456"
    Then she should see a message of add watch list Success!

  Scenario: see the watchlist's ("Tianning") table
    Given a user visits the new watchlist page
    And she should see the title of "Tiannning"


  Scenario: Enter personal page to choose function
     Given a user visits the new watchlist page
     And she should see the title of "Tiannning"
     And she click the user of Tianning and see the functions



