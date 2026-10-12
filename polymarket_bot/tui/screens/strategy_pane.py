"""Strategy pane — run the engine, list signals."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from polymarket_bot.core.models import Signal
from polymarket_bot.tui.widgets import SignalList


class StrategyPane(Vertical):
    DEFAULT_CSS = """
    StrategyPane { padding: 1 2; }
    StrategyPane SignalList { margin-top: 1; padding: 1 1; border: round $panel; height: 1fr; }
    """

    def show(self, signals: list[Signal], enabled: tuple[str, ...]) -> None:
        self.query_one("#strategy-meta", Static).update(
            f"Enabled: [bold]{', '.join(enabled)}[/]   "
            f"[dim]press [/][b]s[/][dim] to re-scan[/]"
        )
        self.query_one(SignalList).show(signals)

    def compose(self) -> ComposeResult:
        yield Static("🧠  STRATEGY", classes="pane-title")
        yield Static(id="strategy-meta")
        yield SignalList()
