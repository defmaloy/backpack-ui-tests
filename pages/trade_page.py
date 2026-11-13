from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.components.order_book import OrderBook
from pages.components.order_form import OrderForm


class TradePage(BasePage):
    """The trade page of one market, built from components (order book, order form)."""

    # The address of the page, added to base_url from pytest.ini
    PATH = "/trade/SOL_USD_PERP"

    # Keeps the browser tab and creates the page's components
    def __init__(self, page: Page):
        super().__init__(page)             # BasePage keeps the tab
        self.order_book = OrderBook(page)  # the page "has" an order book
        self.order_form = OrderForm(page)  # the page "has" an order form