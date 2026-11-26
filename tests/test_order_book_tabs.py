from playwright.sync_api import expect
import pytest

# Marks every test in this file as regression (P2): kept out of the CI smoke run
pytestmark = pytest.mark.regression


# State transition: Book -> click "Trades" -> Trades view
# Checks the "before" state, then that the panel shows recent trades instead of price levels
def test_trades_tab_shows_recent_trades(trade_page):
    book = trade_page.order_book

    # Before: "Book" is the selected tab and its columns are on screen
    expect(book.book_tab).to_have_attribute("aria-selected", "true")
    expect(book.size_header).to_be_visible()
    expect(book.qty_header).to_be_hidden()

    book.open_trades()

    # After: "Trades" is selected, its columns and trade times are on screen
    expect(book.trades_tab).to_have_attribute("aria-selected", "true")
    expect(book.book_tab).to_have_attribute("aria-selected", "false")
    expect(book.qty_header).to_be_visible()
    expect(book.trade_times.first).to_be_visible()

    # And the Book-only columns are gone
    expect(book.size_header).to_be_hidden()
    expect(book.total_header).to_be_hidden()


# State transition: Trades -> click "Book" -> Book view (round trip)
# Checks that going back restores the price levels
def test_book_tab_returns_to_price_levels(trade_page):
    book = trade_page.order_book

    # Before: switch to Trades and make sure it is selected
    book.open_trades()
    expect(book.trades_tab).to_have_attribute("aria-selected", "true")

    book.open_book()

    # After: "Book" is selected again and its columns are back
    expect(book.book_tab).to_have_attribute("aria-selected", "true")
    expect(book.trades_tab).to_have_attribute("aria-selected", "false")
    expect(book.size_header).to_be_visible()
    expect(book.total_header).to_be_visible()
    expect(book.qty_header).to_be_hidden()
