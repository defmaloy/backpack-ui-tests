from playwright.sync_api import Page


class AppSidebar:
    """The left sidebar of the app pages: Home, Trade (Spot, Futures), Lend, Tools, Collapse."""

    # Describes how to find the sidebar's elements (nothing is searched yet)
    def __init__(self, page: Page):
        # The sidebar is a <nav> without a name; it is the one with the "Home" link
        self.root = page.get_by_role("navigation").filter(
            has=page.get_by_role("link", name="Home", exact=True)
        )

        # "Spot" under "Trade": opens the spot market (the market can change)
        self.spot_link = self.root.get_by_role("link", name="Spot", exact=True)

        # One button at the bottom; its name tells the state of the sidebar
        self.collapse_button = self.root.get_by_role("button", name="Collapse sidebar", exact=True)
        self.expand_button = self.root.get_by_role("button", name="Expand sidebar", exact=True)

    # Opens the spot market from the sidebar
    def open_spot(self):
        self.spot_link.click()

    # Makes the sidebar narrow: icons only
    def collapse(self):
        self.collapse_button.click()

    # Makes the sidebar wide again: icons with labels
    def expand(self):
        self.expand_button.click()
