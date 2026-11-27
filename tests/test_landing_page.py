import re

import pytest
from playwright.sync_api import expect

from tests.data import FAKE_EMAIL

# Marks every test in this file as smoke (P1)
pytestmark = pytest.mark.smoke


# Checks that the header "Log in" and "Sign up" links are visible and lead to the right pages
def test_header_has_log_in_and_sign_up_links(landing_page):
    header = landing_page.header

    expect(header.log_in_link).to_be_visible()
    expect(header.sign_up_link).to_be_visible()
    expect(header.log_in_link).to_have_attribute("href", "/login")
    expect(header.sign_up_link).to_have_attribute("href", "/signup")


# Checks that the Trade menu is closed at first, then opens and shows its markets.
# Stocks is not checked: the site hides it for some countries (e.g. the US, where CI runs)
def test_trade_menu_shows_markets(landing_page):
    header = landing_page.header

    # Before: the menu is closed, its links are hidden
    expect(header.trade_menu_crypto).to_be_hidden()

    header.open_trade_menu()

    # After: the links shown in every region are visible and lead to the right markets
    expect(header.trade_menu_crypto).to_have_attribute("href", "/trade/BTC_USD")
    expect(header.trade_menu_perpetuals).to_have_attribute("href", "/trade/BTC_USD_PERP")
    expect(header.trade_menu_crypto).to_be_visible()
    expect(header.trade_menu_perpetuals).to_be_visible()


# Checks that the hero email form opens the sign-up page with the email filled in
def test_hero_form_passes_email_to_sign_up(landing_page):
    landing_page.start_sign_up(FAKE_EMAIL)

    # The email travels in the address: @ is written as %40
    expect(landing_page.page).to_have_url(re.compile(r"/signup\?email=test%40example\.com"))
    expect(landing_page.page.get_by_label("Email", exact=True)).to_have_value(FAKE_EMAIL)
