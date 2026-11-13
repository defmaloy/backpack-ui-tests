import re

from playwright.sync_api import expect


# Checks that the order book has both tabs: "Book" and "Trades"
def test_order_book_tabs_are_visible(trade_page):
    expect(trade_page.order_book.book_tab).to_be_visible()
    expect(trade_page.order_book.trades_tab).to_be_visible()


# Checks that the order book shows the "Price (USD)" column header
def test_order_book_shows_price_column(trade_page):
    expect(trade_page.order_book.price_header).to_be_visible()


# Checks that the order book has loaded data: at least one number is on screen
def test_order_book_shows_numbers(trade_page):
    expect(trade_page.order_book.number_cells.first).to_be_visible()


# Checks that the browser tab title shows the live price and the market name
def test_title_shows_live_price(trade_page):
    # Title looks like: "▲ 82.02 | SOL-PERP (Solana) Futures | Backpack"
    expect(trade_page.page).to_have_title(re.compile(r"\d+\.\d+ \| SOL-PERP"))


# Checks that a guest sees "Sign up" and "Log in" links instead of an order button
def test_guest_sees_login_links_in_order_form(trade_page):
    form = trade_page.order_form

    expect(form.sign_up_link).to_be_visible()
    expect(form.log_in_link).to_be_visible()

    # The links lead to the right pages (checked without clicking)
    expect(form.sign_up_link).to_have_attribute("href", "/signup")
    expect(form.log_in_link).to_have_attribute("href", "/login")