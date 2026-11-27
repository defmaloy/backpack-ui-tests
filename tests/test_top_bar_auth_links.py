import re

import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.signup_page import SignUpPage

# Marks every test in this file as regression (P2): kept out of the CI smoke run
pytestmark = pytest.mark.regression


# Use case testing: a guest on the trade page follows a top bar link.
# Only the navigation LINK is clicked; nothing is typed or submitted on the new page.
# Checks the address and one element that proves the right page loaded.
def test_log_in_link_opens_login_page(trade_page):
    trade_page.top_bar.log_in_link.click()

    expect(trade_page.page).to_have_url(re.compile(r"/login$"))
    expect(LoginPage(trade_page.page).email_input).to_be_visible()


# Use case testing: a guest on the trade page follows the "Sign up" link
def test_sign_up_link_opens_signup_page(trade_page):
    trade_page.top_bar.sign_up_link.click()

    expect(trade_page.page).to_have_url(re.compile(r"/signup$"))
    expect(SignUpPage(trade_page.page).heading).to_be_visible()
