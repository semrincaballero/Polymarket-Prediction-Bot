"""Open-positions table (USDC)."""

from __future__ import annotations

from textual.widgets import DataTable

from polymarket_bot.core.models import Position


class PositionTable(DataTable):
    def __init__(self) -> None:
        super().__init__(cursor_type="row", zebra_stripes=True)

    def on_mount(self) -> None:  # type: ignore[override]
        self.add_columns("Slug", "Side", "Size", "Avg cost", "Last", "Notional $", "uPnL $")

    def show_positions(self, positions: list[Position]) -> None:
        self.clear()
        for p in positions:
            self.add_row(
                p.slug, p.side.value, f"{p.size:,.0f}", f"{p.avg_cost:.3f}",
                f"{p.last_price:.3f}", f"${p.notional_usd:,.0f}", f"${p.upnl_usd:+,.2f}",
            )
