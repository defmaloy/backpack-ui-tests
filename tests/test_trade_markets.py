import re

from playwright.sync_api import Page, expect
import pytest

from pages.trade_page import TradePage

# Marks every test in this file as regression (P2): kept out of the CI smoke run
pytestmark = pytest.mark.regression


# Equivalence partitioning: one market per market type (crypto spot, crypto perpetual).
# Same base asset (BTC), so only the market type changes between the cases.
# Stock perpetuals (e.g. MU.US_USD_PERP) are left out on purpose: hidden for US visitors.
@pytest.mark.parametrize(
    "market, title_end",
    [
        ("BTC_USD", r"BTC/USD \(Bitcoin\) Spot \| Backpack$"),
        ("BTC_USD_PERP", r"BTC-PERP \(Bitcoin\) Futures \| Backpack$"),
    ],
    ids=["crypto-spot", "crypto-perp"],
)
# Checks the address, the title and the order book.
# The title alone is not enough: an unknown market still gets a proper-looking title.
def test_trade_page_opens_for_market(page: Page, market, title_end):
    trade_page = TradePage(page, market)
    trade_page.open()

    # The site did not redirect us to another page
    expect(page).to_have_url(re.compile(rf"/trade/{re.escape(market)}$"))

    # Match only the end of the title: the live price in front comes and goes
    expect(page).to_have_title(re.compile(title_end))

    # A real market loaded: its order book is on screen
    expect(trade_page.order_book.book_tab).to_be_visible()
    expect(trade_page.order_book.price_header).to_be_visible()
