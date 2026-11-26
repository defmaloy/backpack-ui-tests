from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.components.order_book import OrderBook
from pages.components.order_form import OrderForm


class TradePage(BasePage):
    """The trade page of one market, built from components (order book, order form)."""

    # Keeps the browser tab, picks the market and creates the page's components
    def __init__(self, page: Page, market: str = "SOL_USD_PERP"):
        super().__init__(page)             # BasePage keeps the tab
        self.PATH = f"/trade/{market}"     # e.g. /trade/BTC_USD, added to base_url
        self.order_book = OrderBook(page)  # the page "has" an order book
        self.order_form = OrderForm(page)  # the page "has" an order form