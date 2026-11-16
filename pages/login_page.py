from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    """The Log in page: email and password form, no header."""

    # The address of the page, added to base_url from pytest.ini
    PATH = "/login"

    # Describes how to find the form's elements (nothing is searched yet)
    def __init__(self, page: Page):
        super().__init__(page)

        # Fields, found by their visible labels.
        # exact=True: skip the "Show password" eye button
        self.email_input = page.get_by_label("Email", exact=True)
        self.password_input = page.get_by_label("Password", exact=True)

        # Role "button": skip the "Log in" heading above the form
        self.log_in_button = page.get_by_role("button", name="Log in", exact=True)

    # Fills the form without submitting it
    def fill_form(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)