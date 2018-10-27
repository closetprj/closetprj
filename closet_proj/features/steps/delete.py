from behave import given, when, then, use_step_matcher
#from hamcrest import *
import re
from login_utils import *
import time
then
@given(u'a user visits the watchlist site')
def watchlist_site(context):
    pass


@when(u'she would see delete bottom behind admin link and clicks delete')
def delete_admin(context):
    context.browser.get(context.server_address + "/deletewatchlist?name=delete_Tianning_1")

@then(u'she would see delete success')
def delete_success(context):
    pass

@then(u'she would see delete watch list Success!')
def delete_watchlist_Success(context):
   pass