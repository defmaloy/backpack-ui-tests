from playwright.sync_api import Page

from pages.base_page import BasePage


class MarketsPage(BasePage):
    """The Markets page /markets: the "Market Overview" block and the Movers (Gainers / Losers) tabs."""

    # The address of the page, added to base_url from pytest.ini
    PATH = "/markets"

    # Describes how to find the page's elements (nothing is searched yet)
    def __init__(self, page: Page):
        super().__init__(page)

        # The heading of the overview block. The page's main <h1> is not used:
        # its text ("...US Stock Markets") may differ by region.
        self.overview_heading = page.get_by_role("heading", name="Market Overview", exact=True)

        # The page has several tablists (Movers, TradFi, Crypto; "Perps" appears twice),
        # so the tabs are searched only inside the "Movers" tablist
        movers = page.get_by_role("tablist", name="Movers", exact=True)
        self.gainers_tab = movers.get_by_role("tab", name="Gainers", exact=True)
        self.losers_tab = movers.get_by_role("tab", name="Losers", exact=True)

    # Shows the markets that fell the most
    def open_losers(self):
        self.losers_tab.click()

    # Shows the markets that rose the most (the default tab)
    def open_gainers(self):
        self.gainers_tab.click()
