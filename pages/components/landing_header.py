from playwright.sync_api import Page


class LandingHeader:
    """The header of the landing page: product menus, Log in and Sign up."""

    # Describes how to find the header's elements (nothing is searched yet)
    def __init__(self, page: Page):
        # Search only inside <header>: the page has a 2nd "Sign up" in the hero form
        self.root = page.locator("header")

        # Right side: Log in / Sign up
        self.log_in_link = self.root.get_by_role("link", name="Log in", exact=True)
        self.sign_up_link = self.root.get_by_role("link", name="Sign up", exact=True)

        # Middle: the product menu, <nav aria-label="Products">
        self.nav = self.root.get_by_role("navigation", name="Products")
        self.trade_menu_button = self.nav.get_by_role("button", name="Trade", exact=True)

        # Links inside the Trade menu (hidden until the menu opens).
        # The menu differs by country: US visitors get no Stocks item and a shorter
        # Perpetuals description. These names match the text common to all regions.
        self.trade_menu_crypto = self.nav.get_by_role(
            "link", name="Crypto Spot markets and Convert"
        )
        # Contains-match: "...Perps on crypto" (US) and "...Perps on crypto and stocks"
        self.trade_menu_perpetuals = self.nav.get_by_role(
            "link", name="Perpetuals Perps on crypto"
        )

    # Opens the Trade menu the way a user does: the mouse over "Trade"
    def open_trade_menu(self):
        self.trade_menu_button.hover()