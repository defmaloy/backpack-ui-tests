from playwright.sync_api import Page


class AppTopBar:
    """The top bar of the app pages (e.g. the trade page): market search, Log in and Sign up."""

    # Describes how to find the top bar's elements (nothing is searched yet)
    def __init__(self, page: Page):
        # Contains-match on purpose: the full name ends with the "/" shortcut hint
        self.search_button = page.get_by_role("button", name="Search markets, stocks, and more")

        # The bar has no <header> or id, so we describe it by what it contains:
        # a block with the search button AND a "Log in" link.
        # Several nested blocks match; .last is the smallest one.
        # This also skips the "Log in to trade" link in the order form.
        self.root = (
            page.locator("div")
            .filter(has=self.search_button)
            .filter(has=page.get_by_role("link", name="Log in", exact=True))
            .last
        )

        # Right side: links to the Log in and Sign up pages
        self.log_in_link = self.root.get_by_role("link", name="Log in", exact=True)
        self.sign_up_link = self.root.get_by_role("link", name="Sign up", exact=True)

    # Opens the market search dialog
    def open_search(self):
        self.search_button.click()
