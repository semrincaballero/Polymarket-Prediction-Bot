"""Strategy signal list (Static)."""

from __future__ import annotations

from textual.widgets import Static

from polymarket_bot.core.models import Signal

_ICON = {"prob-edge": "◆", "imbalance": "▲", "liquidity": "◯"}


class SignalList(Static):
    def show(self, signals: list[Signal]) -> None:
        if not signals:
            self.update("[dim]no signals — press [b]s[/] to scan the watchlist[/]")
            return
        lines = []
        for s in sorted(signals, key=lambda x: x.confidence, reverse=True):
            color = "green" if s.side.value == "YES" else "red"
            arrow = "▲" if s.side.value == "YES" else "▼"
            icon = _ICON.get(s.kind.value, "•")
            lines.append(
                f"[bold]{icon}[/] [bold]{s.slug:22}[/] "
                f"[bold]{s.kind.value:10}[/] [{color}]{arrow} {s.side.value}[/] "
                f"[dim]conf {s.confidence:.2f}[/]  {s.detail}"
            )
        self.update("\n".join(lines))
