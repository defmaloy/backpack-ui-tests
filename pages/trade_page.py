from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.components.app_sidebar import AppSidebar
from pages.components.app_top_bar import AppTopBar
from pages.components.market_search import MarketSearch
from pages.components.order_book import OrderBook
from pages.components.order_form import OrderForm


class TradePage(BasePage):
    """The trade page of one market, built from components (top bar, sidebar, order book, order form)."""

    # Keeps the browser tab, picks the market and creates the page's components
    def __init__(self, page: Page, market: str = "SOL_USD_PERP"):
        super().__init__(page)             # BasePage keeps the tab
        self.PATH = f"/trade/{market}"     # e.g. /trade/BTC_USD, added to base_url
        self.order_book = OrderBook(page)  # the page "has" an order book
        self.order_form = OrderForm(page)  # the page "has" an order form
        self.top_bar = AppTopBar(page)     # search, Log in, Sign up
        self.search = MarketSearch(page)   # the dialog the search button opens
        self.sidebar = AppSidebar(page)    # left menu: Home, Trade, Spot, ...

        # What the page shows instead of a market when the address is unknown.
        # Plain text (not a heading), searched inside <main>
        self.market_not_found = page.get_by_role("main").get_by_text("Market Not Found", exact=True)
