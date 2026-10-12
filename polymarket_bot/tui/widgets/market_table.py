"""Markets browser table."""

from __future__ import annotations

from textual.widgets import DataTable

from polymarket_bot.core.models import Market


class MarketTable(DataTable):
    def __init__(self) -> None:
        super().__init__(cursor_type="row", zebra_stripes=True)

    def on_mount(self) -> None:  # type: ignore[override]
        self.add_columns("Slug", "Question", "Category", "Price", "Yes bid",
                         "Yes ask", "Spread", "Volume", "Resolve")

    def show_markets(self, markets: list[Market]) -> None:
        self.clear()
        for m in markets:
            self.add_row(
                m.slug, m.question[:34], m.category, f"{m.price:.2f}",
                f"{m.yes_bid:.2f}", f"{m.yes_ask:.2f}", f"{m.spread * 100:.1f}¢",
                f"{m.volume_usd / 1e6:.2f}M", m.ttr_str(), key=m.slug,
            )
