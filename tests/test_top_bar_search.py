import re

import pytest
from playwright.sync_api import expect

# Marks every test in this file as regression (P2): kept out of the CI smoke run
pytestmark = pytest.mark.regression


# Equivalence partitioning: one search result per market type (crypto spot, crypto perpetual).
# Same query and base asset (ETH), so only the market type changes between the cases.
# Stocks are left out on purpose: the site may hide them for US visitors (where CI runs).
# "\/" is an escaped "/": Playwright breaks on a bare "/" inside a regex.
@pytest.mark.parametrize(
    "result_pattern, market",
    [
        (r"ETH\/USD Ethereum", "ETH_USD"),
        (r"ETH-PERP .*Ethereum", "ETH_USD_PERP"),
    ],
    ids=["crypto-spot", "crypto-perp"],
)
# Checks that searching "ETH" and picking a result opens that market's trade page
def test_search_opens_market(trade_page, result_pattern, market):
    search = trade_page.search

    # Before: the search dialog is closed
    expect(search.root).to_be_hidden()

    trade_page.top_bar.open_search()
    search.search("ETH")
    search.result(result_pattern).click()

    # After: the chosen market is open and its order book is on screen
    expect(trade_page.page).to_have_url(re.compile(rf"/trade/{market}$"))
    expect(trade_page.order_book.book_tab).to_be_visible()


# Error guessing: a query that matches nothing must show no market results.
# The site offers an "AI Search" suggestion instead; it is never clicked.
def test_search_without_match_shows_no_markets(trade_page):
    search = trade_page.search

    trade_page.top_bar.open_search()

    # Before: with an empty query the dialog lists markets
    expect(search.market_results.first).to_be_visible()

    search.search("zzqqxx")

    # After: no "Markets" group and no market rows
    expect(search.markets_group).to_be_hidden()
    expect(search.market_results).to_have_count(0)
