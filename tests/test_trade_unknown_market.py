import re

import pytest
from playwright.sync_api import Page, expect

from pages.trade_page import TradePage

# Marks every test in this file as regression (P2 and P3): kept out of the CI smoke run
pytestmark = pytest.mark.regression

# A made-up ticker that exists in no region (not a real stock or token)
UNKNOWN_MARKET = "NOTREAL_USD"


# Error guessing: a user types or bookmarks a market that does not exist.
# Negative test: the page must say so instead of showing a broken or empty market.
def test_unknown_market_shows_not_found(page: Page):
    trade_page = TradePage(page, UNKNOWN_MARKET)
    trade_page.open()

    # The site did not redirect us to another page
    expect(page).to_have_url(re.compile(rf"/trade/{UNKNOWN_MARKET}$"))

    # The page shows the error message
    expect(trade_page.market_not_found).to_be_visible()

    # And no market loaded: the order book is not on the page at all
    expect(trade_page.order_book.book_tab).to_have_count(0)
