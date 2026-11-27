import re

from playwright.sync_api import Page


class OrderBook:
    """The order book panel on the trade page: the Book / Trades tabs and the price list."""

    # Describes how to find the order book's elements (nothing is searched yet)
    def __init__(self, page: Page):
        # The two tabs at the top of the panel
        self.book_tab = page.get_by_role("tab", name="Book", exact=True)
        self.trades_tab = page.get_by_role("tab", name="Trades", exact=True)

        # The panel has no id, so we describe it by what it contains:
        # a block with the "Book" tab AND the "Price (USD)" text.
        # Several nested blocks match; .last is the smallest one.
        self.root = page.locator("div").filter(has=self.book_tab).filter(has_text="Price (USD)").last

        # Two "Price (USD)" texts exist (Book and hidden Trades); take the visible one
        self.price_header = self.root.get_by_text("Price (USD)", exact=True).filter(visible=True)

        # Cells with numbers like 82.08 or 2,664.07 (pattern, not value)
        self.number_cells = self.root.locator("p").filter(has_text=re.compile(r"^[\d,]+\.\d+$"))

        # Column headers that only the "Book" view shows
        self.size_header = self.root.get_by_role("button", name="Size (SOL)", exact=True)
        self.total_header = self.root.get_by_role("button", name="Total (SOL)", exact=True)

        # Column header that only the "Trades" view shows
        self.qty_header = self.root.get_by_role("button", name="Qty (SOL)", exact=True)

        # Time cells of recent trades, like 00:46:59 (pattern, not value).
        # Only the "Trades" view has them; take the visible ones.
        self.trade_times = self.root.get_by_text(re.compile(r"^\d{2}:\d{2}:\d{2}$")).filter(visible=True)

    # Switches the panel to the list of recent trades
    def open_trades(self):
        self.trades_tab.click()

    # Switches the panel back to the price levels (the default view)
    def open_book(self):
        self.book_tab.click()
