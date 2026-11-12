from playwright.sync_api import Page


class BasePage:
    """Parent class for all page objects."""

    # Each child page sets its own path, for example "/login"
    PATH = "/"

    def __init__(self, page: Page):
        # Keep the browser tab, so every method can use it
        self.page = page

    def open(self):
        # base_url from pytest.ini + PATH = the full address.
        # "domcontentloaded": don't wait for every chart and image
        self.page.goto(self.PATH, wait_until="domcontentloaded")