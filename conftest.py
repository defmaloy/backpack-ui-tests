import pytest
from playwright.sync_api import Page

from pages.trade_page import TradePage


@pytest.fixture
def trade_page(page: Page) -> TradePage:
    # Arrange for every test: create the page object and open the page
    trade_page = TradePage(page)
    trade_page.open()
    return trade_page