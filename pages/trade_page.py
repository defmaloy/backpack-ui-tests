from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.components.order_book import OrderBook


class TradePage(BasePage):
    PATH = "/trade/SOL_USD_PERP"

    def __init__(self, page: Page):
        super().__init__(page)             # BasePage keeps the tab
        self.order_book = OrderBook(page)  # the page "has" an order book