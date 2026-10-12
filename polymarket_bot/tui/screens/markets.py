"""Markets browser pane."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from polymarket_bot.core.models import Market
from polymarket_bot.tui.widgets import MarketTable


class MarketsPane(Vertical):
    DEFAULT_CSS = """
    MarketsPane { padding: 1 2; }
    MarketsPane MarketTable { height: 1fr; margin-top: 1; }
    """

    def show(self, markets: list[Market]) -> None:
        self.query_one(MarketTable).show_markets(markets)
        self.query_one("#markets-meta", Static).update(
            f"[dim]{len(markets)} markets · [/][b]/[/][dim] filter · [/]"
            "[b]Enter[/][dim] book · [/][b]s[/][dim] scan[/]"
        )

    def compose(self) -> ComposeResult:
        yield Static("🔍  MARKETS", classes="pane-title")
        yield Static(id="markets-meta")
        yield MarketTable()
