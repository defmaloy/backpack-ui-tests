from playwright.sync_api import expect
import pytest

# Marks every test in this file as regression (P2): kept out of the CI smoke run
pytestmark = pytest.mark.regression


# State transition: More menu closed -> mouse over "More" -> open.
# Checks only items that are not tied to a region (no "Backpack in the USA",
# BP Token or VIP), because CI runs from the US and sees a different landing page.
def test_more_menu_shows_items(landing_page):
    header = landing_page.header

    # Before: the menu is closed, its links are hidden
    expect(header.more_menu_stats).to_be_hidden()

    header.open_more_menu()

    # After: the items are visible and lead to the right pages
    expect(header.more_menu_stats).to_be_visible()
    expect(header.more_menu_reserves).to_be_visible()
    expect(header.more_menu_support).to_be_visible()
    expect(header.more_menu_api).to_be_visible()

    expect(header.more_menu_stats).to_have_attribute("href", "/stats")
    expect(header.more_menu_reserves).to_have_attribute("href", "/reserves")
    expect(header.more_menu_support).to_have_attribute("href", "https://support.backpack.exchange")
    expect(header.more_menu_api).to_have_attribute("href", "https://docs.backpack.exchange/")
