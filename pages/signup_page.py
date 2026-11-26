from playwright.sync_api import Page

from pages.base_page import BasePage


class SignUpPage(BasePage):
    """The Sign up page: email, password, Terms checkbox and the "Open account" button."""

    # The address of the page, added to base_url from pytest.ini
    PATH = "/signup"

    # Describes how to find the form's elements (nothing is searched yet)
    def __init__(self, page: Page):
        super().__init__(page)

        self.heading = page.get_by_role("heading", name="Open your account.", exact=True)

        # Fields, found by their visible labels.
        # exact=True: skip the "Show password" eye button
        self.email_input = page.get_by_label("Email", exact=True)
        self.password_input = page.get_by_label("Password", exact=True)
        self.terms_checkbox = page.get_by_role(
            "checkbox", name="I agree to the Terms and Privacy Policy"
        )

        # The button reads "Loading…" first, then "Open account".
        # We find it only by its final name, so tests wait until it is ready.
        # Tests only check if it is enabled: it is never clicked.
        self.open_account_button = page.get_by_role("button", name="Open account", exact=True)

    # Fills the form without submitting it; empty values are left untouched
    def fill_form(self, email: str, password: str, accept_terms: bool):
        if email:
            self.email_input.fill(email)
        if password:
            self.password_input.fill(password)
        if accept_terms:
            self.terms_checkbox.check()
