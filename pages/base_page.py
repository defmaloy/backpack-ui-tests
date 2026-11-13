from playwright.sync_api import Page


class BasePage:
    """Parent class for all page objects: keeps the browser tab and opens the page."""

    # Each child page sets its own path, for example "/login"
    PATH = "/"

    # Keeps the browser tab, so every method can use it
    def __init__(self, page: Page):
        self.page = page

    # Opens the page in the browser: base_url from pytest.ini + PATH
    def open(self):
        # "domcontentloaded": don't wait for every chart and image
        self.page.goto(self.PATH, wait_until="domcontentloaded")