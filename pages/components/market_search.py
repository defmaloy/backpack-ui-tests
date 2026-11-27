import re

from playwright.sync_api import Page


class MarketSearch:
    """The market search dialog that the top bar's search button opens."""

    # Describes how to find the dialog's elements (nothing is searched yet)
    def __init__(self, page: Page):
        self.search_input = page.get_by_role("searchbox", name="Search a ticker or name")

        # The dialog's name is just "Modal", so we find it by its search field
        self.root = page.get_by_role("dialog").filter(has=self.search_input)

        # The list of results, and the "Markets" group that holds found markets.
        # With no match, the site shows only an "AI Search" suggestion instead.
        self.results = self.root.get_by_role("listbox", name="Markets")
        self.markets_group = self.results.get_by_role("group", name="Markets", exact=True)

        # Found markets have a "/" (ETH/USD) or "-PERP" (ETH-PERP) in their name.
        # Write "/" as "\/" in these patterns: Playwright puts the regex between
        # slashes (/.../) and an unescaped "/" breaks the selector.
        self.market_results = self.results.get_by_role("option", name=re.compile(r"\/USD|-PERP"))

    # Returns one result row, matched by a pattern: the names also hold live prices.
    # A "/" in the pattern must be written as "\/" (see market_results).
    def result(self, name_pattern: str):
        return self.results.get_by_role("option", name=re.compile(name_pattern))

    # Types a query into the search field
    def search(self, text: str):
        self.search_input.fill(text)
