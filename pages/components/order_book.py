import re

from playwright.sync_api import Page


class OrderBook:
    """The order book panel on the trade page."""

    def __init__(self, page: Page):
        self.book_tab = page.get_by_role("tab", name="Book", exact=True)
        self.trades_tab = page.get_by_role("tab", name="Trades", exact=True)

        # The panel has no id, so we describe it by what it contains:
        # a block with the "Book" tab AND the "Price (USD)" text.
        # Several nested blocks match; .last is the smallest one.
        self.root = (
            page.locator("div")
            .filter(has=self.book_tab)
            .filter(has_text="Price (USD)")
            .last
        )

        # Two "Price (USD)" texts exist (Book and hidden Trades); take the visible one
        self.price_header = self.root.get_by_text("Price (USD)", exact=True).filter(
            visible=True
        )

        # Cells with numbers like 82.08 or 2,664.07 (pattern, not value)
        self.number_cells = self.root.locator("p").filter(
            has_text=re.compile(r"^[\d,]+\.\d+$")
        )