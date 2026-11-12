from playwright.sync_api import Page


class OrderBook:
    """The order book panel on the trade page."""

    def __init__(self, page: Page):
        # Locators only describe HOW to find an element.
        # Nothing is searched until a test uses them.
        self.book_tab = page.get_by_role("tab", name="Book", exact=True)
        self.trades_tab = page.get_by_role("tab", name="Trades", exact=True)