"""Dashboard pane — wallet summary + top signals + widest spreads."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from polymarket_bot.core.models import Market, Position, Signal


class DashboardPane(Vertical):
    DEFAULT_CSS = """
    DashboardPane { padding: 1 2; }
    DashboardPane Static#dash-signals { padding: 1 1; border: round $panel; margin-top: 1; }
    DashboardPane Static#dash-spreads { padding: 1 1; border: round $panel; margin-top: 1; }
    """

    def show(self, *, balance_usdc: float, positions: list[Position],
             signals: list[Signal], markets: list[Market]) -> None:
        exposure = sum(p.notional_usd for p in positions)
        pnl = sum(p.upnl_usd for p in positions)
        self.query_one("#dash-summary", Static).update(
            f"Wallet: [bold]paper[/] · {balance_usdc:,.0f} USDC   "
            f"Open: [bold]{exposure:,.0f} USDC[/]   "
            f"Day P&L: [{'green' if pnl >= 0 else 'red'}]{pnl:+,.2f} USDC[/]   "
            f"Signals: [bold]{len(signals)}[/]"
        )
        top = sorted(signals, key=lambda s: s.confidence, reverse=True)[:5]
        sig_txt = "\n".join(
            f"[bold]{s.kind.value:9}[/] {s.slug:22} "
            f"[{'green' if s.side.value == 'YES' else 'red'}]{s.side.value}[/] conf {s.confidence:.2f}"
            for s in top
        ) if top else "[dim]no active signals[/]"
        self.query_one("#dash-signals", Static).update(f"TOP SIGNALS\n{sig_txt}")

        widest = sorted(markets, key=lambda m: m.spread, reverse=True)[:5]
        sp_txt = "\n".join(f"{m.slug:24} spread [red]{m.spread * 100:.1f}¢[/]  "
                           f"vol {m.volume_usd / 1e6:.2f}M  resolve {m.ttr_str()}" for m in widest)
        self.query_one("#dash-spreads", Static).update(f"WIDEST SPREADS\n{sp_txt}")

    def compose(self) -> ComposeResult:
        yield Static("🔮  DASHBOARD", classes="pane-title")
        yield Static(id="dash-summary")
        yield Static(id="dash-signals")
        yield Static(id="dash-spreads")
