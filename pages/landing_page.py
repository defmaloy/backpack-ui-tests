from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.components.landing_header import LandingHeader


class LandingPage(BasePage):
    """The main marketing page backpack.exchange/: header, hero with the email form."""

    # The landing page is the root of the site
    PATH = "/"

    # Keeps the browser tab and creates the page's parts
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = LandingHeader(page)

        # Hero: the email field and its "Sign up" button.
        # Searched inside <main>, so the header's "Sign up" is not matched
        hero = page.get_by_role("main")
        self.hero_email_input = hero.get_by_role("textbox", name="Email address")
        self.hero_sign_up_button = hero.get_by_role("button", name="Sign up", exact=True)

    # Types an email in the hero form and clicks "Sign up"
    def start_sign_up(self, email: str):
        self.hero_email_input.fill(email)
        self.hero_sign_up_button.click()