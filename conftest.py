import pytest
from playwright.sync_api import Page, expect

from pages.trade_page import TradePage

# Backpack is a heavy live site: give every expect() 10 s instead of the default 5 s
expect.set_options(timeout=10_000)


# Gives a test the trade page, already opened in a fresh browser tab
@pytest.fixture
def trade_page(page: Page) -> TradePage:
    trade_page = TradePage(page)
    trade_page.open()
    return trade_page