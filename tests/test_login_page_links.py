import re

from playwright.sync_api import expect
import pytest

from pages.forgot_password_page import ForgotPasswordPage
from pages.signup_page import SignUpPage

# Marks every test in this file as regression (P2 and P3): kept out of the CI smoke run
pytestmark = pytest.mark.regression


# Use case testing: a guest on the Log in page follows the "Forgot password?" link.
# Only the navigation LINK is clicked; nothing is typed or submitted on the new page.
# Checks the address before and after, and one element that proves the right page loaded.
def test_forgot_password_link_opens_reset_page(login_page):
    expect(login_page.page).to_have_url(re.compile(r"/login$"))

    login_page.open_forgot_password()

    expect(login_page.page).to_have_url(re.compile(r"/forgot-password$"))
    expect(ForgotPasswordPage(login_page.page).heading).to_be_visible()


# Use case testing: a guest on the Log in page follows the "Open account" link.
# It is a link to /signup, not the "Open account" submit button of the Sign up form.
def test_open_account_link_opens_signup_page(login_page):
    expect(login_page.page).to_have_url(re.compile(r"/login$"))

    login_page.open_sign_up()

    expect(login_page.page).to_have_url(re.compile(r"/signup$"))
    expect(SignUpPage(login_page.page).heading).to_be_visible()
