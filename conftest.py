import pytest
from playwright.sync_api import Page

from pages.trade_page import TradePage


# Gives a test the trade page, already opened in a fresh browser tab
@pytest.fixture
def trade_page(page: Page) -> TradePage:
    trade_page = TradePage(page)
    trade_page.open()
    return trade_page