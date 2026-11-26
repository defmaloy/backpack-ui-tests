from playwright.sync_api import expect
import pytest

from tests.data import FAKE_EMAIL, FAKE_PASSWORD, FAKE_WEAK_PASSWORD

# Marks every test in this file as regression (P2): kept out of the CI smoke run
pytestmark = pytest.mark.regression


# Decision table: 3 conditions (email, password, Terms) -> is "Open account" enabled?
#
#   #  | Email  | Password | Terms | Open account
#   1  | empty  | empty    | no    | disabled (the "before" state)
#   2  | filled | strong   | no    | disabled
#   3  | empty  | strong   | yes   | disabled
#   4  | filled | empty    | yes   | disabled
#   5  | filled | weak     | yes   | disabled
#   6  | filled | strong   | yes   | enabled
#
# The button is only checked, never clicked. Its locator uses the final name
# "Open account", so expect() waits until the "Loading…" button is replaced.
@pytest.mark.parametrize(
    "email, password, accept_terms, enabled",
    [
        ("", "", False, False),
        (FAKE_EMAIL, FAKE_PASSWORD, False, False),
        ("", FAKE_PASSWORD, True, False),
        (FAKE_EMAIL, "", True, False),
        (FAKE_EMAIL, FAKE_WEAK_PASSWORD, True, False),
        (FAKE_EMAIL, FAKE_PASSWORD, True, True),
    ],
    ids=[
        "1-all-empty",
        "2-no-terms",
        "3-no-email",
        "4-no-password",
        "5-weak-password",
        "6-all-filled",
    ],
)
# Checks if "Open account" is enabled for one row of the table
def test_open_account_button_state(signup_page, email, password, accept_terms, enabled):
    signup_page.fill_form(email, password, accept_terms)

    if enabled:
        expect(signup_page.open_account_button).to_be_enabled()
    else:
        expect(signup_page.open_account_button).to_be_disabled()
