import re

import pytest
from playwright.sync_api import expect

# Marks every test in this file as regression (P2): kept out of the CI smoke run
pytestmark = pytest.mark.regression


# State transition: perpetual market -> click "Spot" -> spot market.
# The spot market it opens can change (BTC_USD, SOL_USD...), so we match a pattern:
# a spot market ends with _USD, a perpetual with _USD_PERP.
def test_spot_opens_spot_market(trade_page):
    # Before: we are on a perpetual market (SOL_USD_PERP)
    expect(trade_page.page).to_have_url(re.compile(r"_PERP$"))

    trade_page.sidebar.open_spot()

    # After: a spot market is open and its order book is on screen
    expect(trade_page.page).to_have_url(re.compile(r"/trade/[A-Z]+_USD$"))
    expect(trade_page.page).to_have_title(re.compile(r"Spot \| Backpack$"))
    expect(trade_page.order_book.book_tab).to_be_visible()


# State transition: expanded -> click "Collapse" -> collapsed.
# Checks that the button changes its name and the "Spot" label is hidden.
# The site hides the label by shrinking its wrapper to 0 px height (overflow hidden),
# so the link keeps its own size and to_be_hidden() would still call it "visible".
# not_to_be_in_viewport() checks what the user sees: no part of it is on screen.
def test_collapse_hides_labels(trade_page):
    sidebar = trade_page.sidebar

    # Before: the sidebar is expanded and shows the "Spot" label
    expect(sidebar.collapse_button).to_be_visible()
    expect(sidebar.spot_link).to_be_in_viewport()

    sidebar.collapse()

    # After: the button now offers "Expand" and the label is gone
    expect(sidebar.expand_button).to_be_visible()
    expect(sidebar.collapse_button).to_be_hidden()
    expect(sidebar.spot_link).not_to_be_in_viewport()


# State transition: collapsed -> click "Expand" -> expanded (round trip).
# Checks that expanding brings the "Spot" label back
def test_expand_shows_labels_again(trade_page):
    sidebar = trade_page.sidebar

    # Before: collapse the sidebar and make sure the label is gone
    sidebar.collapse()
    expect(sidebar.expand_button).to_be_visible()
    expect(sidebar.spot_link).not_to_be_in_viewport()

    sidebar.expand()

    # After: the button offers "Collapse" again and the label is back
    expect(sidebar.collapse_button).to_be_visible()
    expect(sidebar.spot_link).to_be_in_viewport()
