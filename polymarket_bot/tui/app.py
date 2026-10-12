"""The Textual application — the Polymarket bot dashboard."""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header, TabbedContent, TabPane

from polymarket_bot.config import Config
from polymarket_bot.core import StrategyEngine
from polymarket_bot.core.mock_data import demo_book, demo_fills, demo_markets, demo_positions
from polymarket_bot.tui.screens import (
    BookPane, DashboardPane, LogPane, MarketsPane, PositionsPane, SettingsPane, StrategyPane,
)

_THEMES = ("textual-dark", "nord", "tokyo-night", "dracula")
_BALANCE_USDC = 12000.0


class PolymarketBotApp(App):
    CSS_PATH = "styles.tcss"
    TITLE = "Polymarket Prediction Bot"
    SUB_TITLE = "browse · book · strategy · positions — paper by default"

    BINDINGS = [
        Binding("1", "tab('dashboard')", "Dash", show=False),
        Binding("2", "tab('markets')", "Markets", show=False),
        Binding("3", "tab('book')", "Book", show=False),
        Binding("4", "tab('strategy')", "Strategy", show=False),
        Binding("5", "tab('positions')", "Positions", show=False),
        Binding("6", "tab('log')", "Log", show=False),
        Binding("7", "tab('settings')", "Settings", show=False),
        Binding("q", "quit", "Quit"),
        Binding("s", "rescan", "Scan"),
        Binding("o", "compose_order", "Order"),
        Binding("t", "cycle_theme", "Theme"),
        Binding("question_mark", "help", "Help", key_display="?"),
    ]

    def __init__(self, config: Config, initial_market: str | None = None) -> None:
        super().__init__()
        self.config = config
        self._engine = StrategyEngine()
        self._markets = demo_markets()
        self._focus_index = 0
        if initial_market:
            for i, m in enumerate(self._markets):
                if m.slug == initial_market:
                    self._focus_index = i
                    break
        self._theme_index = 0
        self._signals = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with TabbedContent(id="tabs", initial="dashboard"):
            yield TabPane("Dash", DashboardPane(), id="dashboard")
            yield TabPane("Markets", MarketsPane(), id="markets")
            yield TabPane("Book", BookPane(), id="book")
            yield TabPane("Strategy", StrategyPane(), id="strategy")
            yield TabPane("Positions", PositionsPane(), id="positions")
            yield TabPane("Log", LogPane(), id="log")
            yield TabPane("Settings", SettingsPane(), id="settings")
        yield Footer()

    def on_mount(self) -> None:  # type: ignore[override]
        self.theme = _THEMES[self._theme_index]
        self._rescan()
        self._push_all()
        self.query_one(SettingsPane).show(self.config)

    # ----------------------------------------------------------------- data flow

    def _rescan(self) -> None:
        sigs = []
        for m in self._markets:
            sigs.extend(self._engine.evaluate(m, demo_book(m)))
        self._signals = sigs

    def _push_all(self) -> None:
        positions = demo_positions(self._markets)
        fills = demo_fills()
        self.query_one(DashboardPane).show(
            balance_usdc=_BALANCE_USDC, positions=positions,
            signals=self._signals, markets=self._markets,
        )
        self.query_one(MarketsPane).show(self._markets)
        self.query_one(BookPane).show(
            self._markets[self._focus_index], demo_book(self._markets[self._focus_index])
        )
        self.query_one(StrategyPane).show(self._signals, self.config.strategies.enabled)
        self.query_one(PositionsPane).show(positions)
        self.query_one(LogPane).show(fills)

    # ------------------------------------------------------------------- actions

    def action_tab(self, pane_id: str) -> None:
        self.query_one(TabbedContent).active = pane_id

    def action_rescan(self) -> None:
        self._rescan()
        self.query_one(StrategyPane).show(self._signals, self.config.strategies.enabled)
        self.query_one(DashboardPane).show(
            balance_usdc=_BALANCE_USDC, positions=demo_positions(self._markets),
            signals=self._signals, markets=self._markets,
        )
        self.notify(f"scanned {len(self._markets)} markets → {len(self._signals)} signals", timeout=2)

    def action_compose_order(self) -> None:
        m = self._markets[self._focus_index]
        self.notify(
            f"paper order · {m.slug} YES @ {m.yes_ask:.2f} × 100 USDC",
            title="Compose (paper)", timeout=4,
        )

    def action_cycle_theme(self) -> None:
        self._theme_index = (self._theme_index + 1) % len(_THEMES)
        self.theme = _THEMES[self._theme_index]
        self.notify(f"theme: {self.theme}", timeout=1)

    def action_help(self) -> None:
        self.notify("1-7 tabs · s scan · o order · t theme · q quit",
                    title="Keybindings", timeout=4)
