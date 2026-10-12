"""Positions pane."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from polymarket_bot.core.models import Position
from polymarket_bot.tui.widgets import PositionTable


class PositionsPane(Vertical):
    DEFAULT_CSS = """
    PositionsPane { padding: 1 2; }
    PositionsPane PositionTable { height: 1fr; margin-top: 1; }
    """

    def show(self, positions: list[Position]) -> None:
        exposure = sum(p.notional_usd for p in positions)
        pnl = sum(p.upnl_usd for p in positions)
        self.query_one("#pos-meta", Static).update(
            f"Open: [bold]{len(positions)}[/]   "
            f"Exposure: [bold]{exposure:,.0f} USDC[/]   "
            f"uPnL: [{'green' if pnl >= 0 else 'red'}]{pnl:+,.2f} USDC[/]"
        )
        self.query_one(PositionTable).show_positions(positions)

    def compose(self) -> ComposeResult:
        yield Static("💼  POSITIONS", classes="pane-title")
        yield Static(id="pos-meta")
        yield PositionTable()
