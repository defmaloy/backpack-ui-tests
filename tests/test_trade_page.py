from playwright.sync_api import expect


def test_order_book_tabs_are_visible(trade_page):
    expect(trade_page.order_book.book_tab).to_be_visible()
    expect(trade_page.order_book.trades_tab).to_be_visible()