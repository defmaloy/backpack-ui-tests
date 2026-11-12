import re

from playwright.sync_api import Page, expect

TRADE_URL = "/trade/SOL_USD_PERP"


# "page" is a built-in fixture from pytest-playwright:
# a fresh browser tab for each test, closed automatically afterwards
def test_trade_page_opens(page: Page):
    # Act: open the page in the browser
    page.goto(TRADE_URL)

    # Assert: the browser tab title mentions Backpack
    expect(page).to_have_title(re.compile("Backpack", re.IGNORECASE))
