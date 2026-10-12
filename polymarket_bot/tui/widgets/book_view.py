"""CLOB book view (Static, rebuilt via update)."""

from __future__ import annotations

from textual.widgets import Static

from polymarket_bot.core.models import ClobBook


class BookView(Static):
    def show(self, book: ClobBook) -> None:
        imb = book.imbalance
        imb_str = f"{'YES-heavy' if imb > 0 else 'NO-heavy'} {abs(imb) * 100:.0f}%"
        lines = [
            f"[bold]YES[/]  bid [green]{book.yes_bids.best:.2f}[/]   "
            f"ask [red]{book.yes_asks.best:.2f}[/]   "
            f"spread {(book.yes_asks.best - book.yes_bids.best) * 100:.1f}¢",
            f"[bold]NO[/]   bid [green]{book.no_bids.best:.2f}[/]   "
            f"ask [red]{book.no_asks.best:.2f}[/]",
            f"imbalance: [cyan]{imb_str}[/]",
            "",
            "[dim]── YES bids / asks (top 5, USDC) ──[/]",
        ]
        for i in range(5):
            b = book.yes_bids.levels[i] if i < len(book.yes_bids.levels) else (0, 0)
            a = book.yes_asks.levels[i] if i < len(book.yes_asks.levels) else (0, 0)
            lines.append(f"  {b[0]:.2f} × ${b[1]:>6,.0f}   |   {a[0]:.2f} × ${a[1]:>6,.0f}")
        self.update("\n".join(lines))
