"""Deterministic demo dataset for ``--demo`` mode."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from polymarket_bot.core.models import BookSide, ClobBook, Fill, Market, Position, Side

_NOW = datetime(2026, 7, 19, 14, 2, tzinfo=timezone.utc)


def demo_markets() -> list[Market]:
    rows = [
        ("btc-100k-by-eoy", "Will BTC hit $100k by end of year", "crypto", 0.31, 3.1e6, 165),
        ("fed-cut-sep", "Will the Fed cut rates in September", "economics", 0.68, 8.4e6, 59),
        ("eth-4k-july", "Will ETH close above $4k in July", "crypto", 0.12, 1.2e6, 12),
        ("us-recession-2026", "Will the US enter recession in 2026", "economics", 0.42, 2.7e6, 198),
        ("sol-250-eoy", "Will SOL hit $250 by end of year", "crypto", 0.54, 1.9e6, 165),
        ("election-turnout-record", "Will 2026 turnout set a record", "politics", 0.37, 4.2e6, 108),
    ]
    out: list[Market] = []
    for slug, q, cat, price, vol, days in rows:
        bid = max(0.01, price - 0.02)
        ask = min(0.99, price + 0.02)
        out.append(Market(slug=slug, question=q, category=cat, price=price, volume_usd=vol,
                          resolve_at=_NOW + timedelta(days=days, hours=4),
                          yes_bid=bid, yes_ask=ask))
    return out


def demo_book(market: Market) -> ClobBook:
    # YES-heavy book (realistic directional skew): thick YES bids + thick NO asks.
    yes_bid_levels = [(market.yes_bid - i * 0.005, 8000 - i * 800) for i in range(5)]
    yes_ask_levels = [(market.yes_ask + i * 0.005, 3000 - i * 300) for i in range(5)]
    no_bid_levels = [(1 - market.yes_ask - i * 0.005, 2500 - i * 250) for i in range(5)]
    no_ask_levels = [(1 - market.yes_bid + i * 0.005, 6000 - i * 600) for i in range(5)]
    return ClobBook(
        slug=market.slug,
        yes_bids=BookSide(yes_bid_levels), yes_asks=BookSide(yes_ask_levels),
        no_bids=BookSide(no_bid_levels), no_asks=BookSide(no_ask_levels),
    )


def demo_positions(markets: list[Market]) -> list[Position]:
    picks = [(markets[0], Side.YES, 4000, 0.25), (markets[1], Side.YES, 3000, 0.60),
             (markets[2], Side.NO, 5000, 0.18), (markets[4], Side.YES, 2000, 0.48)]
    return [Position(slug=m.slug, side=s, size=sh, avg_cost=c, last_price=m.price)
            for m, s, sh, c in picks]


def demo_fills(n: int = 14) -> list[Fill]:
    slugs = [m.slug for m in demo_markets()]
    out: list[Fill] = []
    seed = 7
    for i in range(n):
        seed = (1664525 * seed + 1013904223) & 0x7FFFFFFF
        rnd = seed / 0x7FFFFFFF
        slug = slugs[i % len(slugs)]
        side = Side.YES if rnd > 0.45 else Side.NO
        price = 0.20 + rnd * 0.6
        out.append(Fill(
            time=_NOW - timedelta(hours=n - i, minutes=int(rnd * 50)),
            slug=slug, side=side, size=round(100 + rnd * 900, 2),
            price=round(price, 3), fee_usd=round(price * 2, 2), paper=True,
        ))
    return out


def demo_now() -> datetime:
    return _NOW
