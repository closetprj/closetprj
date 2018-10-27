import re
from login_utils import *
from behave import *

@Given(u'a user home page')
def homepage(context):
    context.browser.get(context.server_address)

@when(u'she logs in and clicks My Lists')
def see_add(context):
    add_found = context.browser.find_element_by_id("My lists")
    add_found.click()
    assert add_found


@then(u'she would see a add button and click it')
def see(context):
    add_found = context.browser.find_element_by_id('test')
    add_found.click()


@When(u'a user visits the new watchlist page')
def enter_add_new(context):
    my_lists = context.browser.find_element_by_id("My lists")
    my_lists.click()
    # add = context.browser.find_element_by_id("add")
    # add.click()
    context.browser.get(context.server_address + "/add")

@then(u'she will enter the add user page')
def add_user_page(context):
    context.browser.get(context.server_address + "/addwatchlist")

@then(u'she write detail with Email "{email}" and Firstname "{firstName}" and Lastname "{lastName}" and gender "{gender}" and Address "{address1}" and Postcode with "{postcode}" and city "{city}" and Phone namber "{phone}"')
def see_addwatchlist(context,email,firstName,lastName,gender,address1,postcode,city,phone):
    context.browser.get(context.server_address + "/registerationForm")
    firstNam = context.browser.find_element_by_name('firstName')
    emai = context.browser.find_element_by_name('email')
    lastNam = context.browser.find_element_by_name('lastName')
    gende = context.browser.find_element_by_name('gender')
    address = context.browser.find_element_by_name('address1')
    postcod = context.browser.find_element_by_name('postcode')
    cit = context.browser.find_element_by_name('city')
    phon = context.browser.find_element_by_name('phone')
    emai.clear()
    firstNam.clear()
    lastNam.clear()
    gende.clear()
    address.clear()
    postcod.clear()
    cit.clear()
    phon.clear()
    emai.send_keys(email)
    firstNam.send_keys(firstName)
    lastNam.send_keys(lastName)
    gende.send_keys(gender)
    address.send_keys(address1)
    postcod.send_keys(postcode)
    cit.send_keys(city)
    phon.send_keys(phone)
    confirm = context.browser.find_element_by_name('confirm')
    confirm.click()

@then(u'she should see a message of add watch list Success!')
def add_successful(context):
    new_found = re.search("add charactor succseess", context.browser.page_source, re.IGNORECASE)
    assert new_found

@given (u'a user visits the new watchlist page')
def add_page(context):
    context.browser.get(context.server_address + "/addwatchlist")
    add_found = context.browser.find_element_by_id("My lists")
    add_found.click()
    assert add_found

@given(u'she should see the title of "Tiannning"')
def newWatchlist_found(context):
    new_found = re.search("Tianning", context.browser.page_source, re.IGNORECASE)
    assert new_found

@given(u'she click the user of Tianning and see the functions')
def function_selection(context):
    context.browser.get(context.server_address + "/addwatchlist")
    add_found = context.browser.find_element_by_id("My lists")
    add_found.click()
    found = context.browser.find_element_by_id('Tianning')
    context.browser.get(context.server_address + "/function?name=tianning_1")