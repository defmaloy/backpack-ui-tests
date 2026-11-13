from playwright.sync_api import Page


class OrderForm:
    """The order form panel on the trade page (right side)."""

    # Describes how to find the order form's elements (nothing is searched yet)
    def __init__(self, page: Page):
         # What a guest (not logged in) sees instead of an order button
        self.sign_up_link = page.get_by_role("link", name="Sign up to trade")
        self.log_in_link = page.get_by_role("link", name="Log in to trade")