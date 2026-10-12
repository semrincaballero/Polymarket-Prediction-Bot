"""CLOB book pane."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from polymarket_bot.core.models import ClobBook, Market
from polymarket_bot.tui.widgets import BookView


class BookPane(Vertical):
    DEFAULT_CSS = """
    BookPane { padding: 1 2; }
    BookPane BookView { margin-top: 1; padding: 1 1; border: round $panel; }
    """

    def show(self, market: Market, book: ClobBook) -> None:
        self.query_one("#book-meta", Static).update(
            f"[bold]{market.slug}[/]   [dim]{market.question}[/]   "
            f"price [bold]{market.price:.2f}[/]   resolve [bold]{market.ttr_str()}[/]"
        )
        self.query_one(BookView).show(book)

    def compose(self) -> ComposeResult:
        yield Static("📖  CLOB ORDER BOOK", classes="pane-title")
        yield Static(id="book-meta")
        yield BookView()
