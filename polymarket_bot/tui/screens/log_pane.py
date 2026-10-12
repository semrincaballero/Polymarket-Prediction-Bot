"""Fill log pane."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import DataTable, Static

from polymarket_bot.core.models import Fill


class LogPane(Vertical):
    DEFAULT_CSS = """
    LogPane { padding: 1 2; }
    LogPane DataTable { height: 1fr; margin-top: 1; }
    """

    def show(self, fills: list[Fill]) -> None:
        self.query_one(DataTable).clear()
        for f in fills:
            tag = "paper" if f.paper else "LIVE"
            self.query_one(DataTable).add_row(
                f.time.strftime("%m-%d %H:%M"), f.slug, f.side.value,
                f"{f.size:,.0f}", f"{f.price:.3f}", f"${f.fee_usd:.2f}", tag,
            )
        self.query_one("#log-meta", Static).update(
            f"[dim]{len(fills)} fills · local paper-trail · live needs credentials[/]"
        )

    def compose(self) -> ComposeResult:
        yield Static("🧾  ORDER LOG", classes="pane-title")
        yield Static(id="log-meta")
        table = DataTable(cursor_type="row", zebra_stripes=True)
        table.add_columns("Time", "Slug", "Side", "Size", "Price", "Fee", "Mode")
        yield table
