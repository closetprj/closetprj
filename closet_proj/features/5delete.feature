# Created by mingting at 2017/5/29
Feature: delete user namely Tianning in account from "admin"

  Scenario: Login Success
    Given a user visits the site
    When a user visits the login page
    And she logs in with username "admin" and password "default"
    Then she should see a message of login success

  Scenario: delete watchlist namely Tianning
    When she logs in and clicks My Lists
    When she would see delete bottom behind admin link and clicks delete
    Given a user visits the new watchlist page
