import re

import pytest
from playwright.sync_api import Page, expect

# Marks every test in this file as smoke (P1)
pytestmark = pytest.mark.smoke

# The address of the trade page, added to base_url from pytest.ini
TRADE_URL = "/trade/SOL_USD_PERP"


# Checks that the trade page opens and the tab title mentions Backpack
def test_trade_page_opens(page: Page):
    page.goto(TRADE_URL)

    expect(page).to_have_title(re.compile("Backpack", re.IGNORECASE))