import pytest
from playwright.sync_api import expect

from tests.data import FAKE_EMAIL, FAKE_PASSWORD

# Marks every test in this file as smoke (P1)
pytestmark = pytest.mark.smoke


# Checks that the form has an email field, a password field and the Log in button
def test_login_form_is_visible(login_page):
    expect(login_page.email_input).to_be_visible()
    expect(login_page.password_input).to_be_visible()
    expect(login_page.log_in_button).to_be_visible()


# Checks that the Log in button is disabled while the form is empty
def test_log_in_button_disabled_when_empty(login_page):
    expect(login_page.log_in_button).to_be_disabled()


# Checks that an email alone is not enough: the button stays disabled
def test_log_in_button_disabled_with_email_only(login_page):
    login_page.email_input.fill(FAKE_EMAIL)

    expect(login_page.log_in_button).to_be_disabled()


# Decision table, row 3: email empty, password filled -> button disabled
def test_log_in_button_disabled_with_password_only(login_page):
    login_page.password_input.fill(FAKE_PASSWORD)

    expect(login_page.log_in_button).to_be_disabled()


# Checks that the button becomes enabled when both fields are filled (never clicked)
def test_log_in_button_enabled_when_form_filled(login_page):
    login_page.fill_form(FAKE_EMAIL, FAKE_PASSWORD)

    expect(login_page.log_in_button).to_be_enabled()