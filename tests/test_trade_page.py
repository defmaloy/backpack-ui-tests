import re

from playwright.sync_api import expect


def test_order_book_tabs_are_visible(trade_page):
    expect(trade_page.order_book.book_tab).to_be_visible()
    expect(trade_page.order_book.trades_tab).to_be_visible()


def test_order_book_shows_price_column(trade_page):
    expect(trade_page.order_book.price_header).to_be_visible()


def test_order_book_shows_numbers(trade_page):
    # At least one number cell is on screen: the book has loaded data
    expect(trade_page.order_book.number_cells.first).to_be_visible()


def test_title_shows_live_price(trade_page):
    # Title looks like: "▲ 82.02 | SOL-PERP (Solana) Futures | Backpack"
    expect(trade_page.page).to_have_title(re.compile(r"\d+\.\d+ \| SOL-PERP"))