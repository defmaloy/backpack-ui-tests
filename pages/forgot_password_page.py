from playwright.sync_api import Page

from pages.base_page import BasePage


class ForgotPasswordPage(BasePage):
    """The Reset password page: one email field and the "Send reset link" button (never clicked)."""

    # The address of the page, added to base_url from pytest.ini
    PATH = "/forgot-password"

    # Describes how to find the page's elements (nothing is searched yet)
    def __init__(self, page: Page):
        super().__init__(page)

        # The page title above the form; proves this page has loaded
        self.heading = page.get_by_role("heading", name="Reset password.", exact=True)
