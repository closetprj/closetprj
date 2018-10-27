# Created by mingting at 12/10/18

Feature: Home Page

  Scenario: Visit homepage
    Given a user visits the site
    Then she should see closet

  Scenario: Login Link
    Given a user visits the site
    Then she should see the Login link

  Scenario: Logout Link
    Given a user visits the site
    When she logs in
    And she returns to the site
    Then she should see the Logout link

  Scenario: Sign up Link
    Given a user visits the site
    And she is logged out
    Then she should see the Sign up link
