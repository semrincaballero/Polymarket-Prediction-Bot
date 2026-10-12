"""Settings pane."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static

from polymarket_bot.config import Config


class SettingsPane(VerticalScroll):
    DEFAULT_CSS = """
    SettingsPane { padding: 1 2; }
    """

    def show(self, config: Config) -> None:
        a, n, r, s = config.auth, config.network, config.risk, config.strategies
        key_set = bool(a.api_key and a.private_key)
        self.query_one("#cfg", Static).update(
            f"[bold cyan]auth[/]\n"
            f"  [dim]proxy_address[/] = {(a.proxy_address[:8] + '…') if a.proxy_address else '[red](not set)[/]'}\n"
            f"  [dim]api_key[/]        = {'[red](not set)[/]' if not key_set else '[green]set[/]'}\n"
            f"  [dim]endpoint[/]       = {a.endpoint}\n"
            f"  [dim]mode[/]           = {'[red]LIVE[/]' if config.live else '[green]paper[/]'}\n\n"
            f"[bold cyan]network[/]\n  [dim]gamma_url[/] = {n.gamma_url}\n\n"
            f"[bold cyan]risk[/]\n"
            f"  [dim]max_exposure[/]     = {r.max_exposure_usd:,.0f} USDC\n"
            f"  [dim]per_market_cap[/]   = {r.per_market_cap_usd:,.0f} USDC\n"
            f"  [dim]daily_loss_limit[/] = {r.daily_loss_limit_usd:,.0f} USDC\n\n"
            f"[bold cyan]strategies[/]  = {', '.join(s.enabled)}\n\n"
            "[dim]Edit ~/.polymarket-bot/config.toml and relaunch.[/]"
        )

    def compose(self) -> ComposeResult:
        yield Static("⚙️  SETTINGS", classes="pane-title")
        yield Static(id="cfg")
