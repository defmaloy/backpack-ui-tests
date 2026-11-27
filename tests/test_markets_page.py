import re

import pytest
from playwright.sync_api import expect

# Marks every test in this file as regression (P2 and P3): kept out of the CI smoke run
pytestmark = pytest.mark.regression

# Region note: these tests ran from outside the US. Whether US visitors (the CI region)
# see the Movers tabs at all is not verified yet. If these tests are ever added to CI,
# check the Movers block from a US runner first.
# Only the tab state (aria-selected) is checked, never the list rows: they hold live
# prices and can mix stocks and crypto depending on the region.


# Basic check that the page opens (no test design technique: one address, nothing to vary).
# Checks the address and the "Market Overview" heading (common to all regions).
def test_markets_page_opens(markets_page):
    expect(markets_page.page).to_have_url(re.compile(r"/markets$"))
    expect(markets_page.overview_heading).to_be_visible()


# State transition: Gainers -> click "Losers" -> Losers selected
# Checks the "before" state, then that the selection moved to the other tab
def test_losers_tab_becomes_selected(markets_page):
    # Before: "Gainers" is the default tab
    expect(markets_page.gainers_tab).to_have_attribute("aria-selected", "true")
    expect(markets_page.losers_tab).to_have_attribute("aria-selected", "false")

    markets_page.open_losers()

    # After: "Losers" is selected, "Gainers" is not
    expect(markets_page.losers_tab).to_have_attribute("aria-selected", "true")
    expect(markets_page.gainers_tab).to_have_attribute("aria-selected", "false")


# State transition: Losers -> click "Gainers" -> Gainers selected (round trip)
# Checks that going back restores the default tab
def test_gainers_tab_becomes_selected_again(markets_page):
    # Before: switch to Losers and make sure it is selected
    markets_page.open_losers()
    expect(markets_page.losers_tab).to_have_attribute("aria-selected", "true")

    markets_page.open_gainers()

    # After: "Gainers" is selected again, "Losers" is not
    expect(markets_page.gainers_tab).to_have_attribute("aria-selected", "true")
    expect(markets_page.losers_tab).to_have_attribute("aria-selected", "false")
