"""Typed models for Polymarket CLOB markets, books, positions and signals."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum


class Side(str, Enum):
    YES = "YES"
    NO = "NO"


class SignalKind(str, Enum):
    PROB_EDGE = "prob-edge"
    IMBALANCE = "imbalance"
    LIQUIDITY = "liquidity"


@dataclass(frozen=True)
class Market:
    slug: str
    question: str
    category: str
    price: float                 # current YES price, 0..1
    volume_usd: float
    resolve_at: datetime
    yes_bid: float
    yes_ask: float

    @property
    def spread(self) -> float:
        return self.yes_ask - self.yes_bid

    @property
    def mid(self) -> float:
        return (self.yes_bid + self.yes_ask) / 2

    def ttr_str(self) -> str:
        now = datetime.now(tz=timezone.utc)
        end = self.resolve_at if self.resolve_at.tzinfo else self.resolve_at.replace(tzinfo=timezone.utc)
        t = end - now
        if t.total_seconds() <= 0:
            return "resolved"
        d = int(t.total_seconds() // 86400)
        h = int((t.total_seconds() % 86400) // 3600)
        return f"{d}d {h:02d}h" if d else f"{h}h"


@dataclass(frozen=True)
class BookSide:
    levels: list[tuple[float, float]] = field(default_factory=list)   # (price, size USDC)

    @property
    def best(self) -> float:
        return self.levels[0][0] if self.levels else 0.0

    @property
    def total_usd(self) -> float:
        return sum(s for _, s in self.levels)


@dataclass(frozen=True)
class ClobBook:
    slug: str
    yes_bids: BookSide
    yes_asks: BookSide
    no_bids: BookSide
    no_asks: BookSide

    @property
    def imbalance(self) -> float:
        """+1 = YES-heavy, −1 = NO-heavy."""
        yes = self.yes_bids.total_usd + self.no_asks.total_usd
        no = self.no_bids.total_usd + self.yes_asks.total_usd
        denom = yes + no
        return (yes - no) / denom if denom else 0.0


@dataclass(frozen=True)
class Position:
    slug: str
    side: Side
    size: float              # number of shares
    avg_cost: float          # per-share USDC cost, 0..1
    last_price: float

    @property
    def notional_usd(self) -> float:
        return self.size * self.avg_cost

    @property
    def upnl_usd(self) -> float:
        sign = 1 if self.side is Side.YES else -1
        return sign * self.size * (self.last_price - self.avg_cost)


@dataclass(frozen=True)
class Signal:
    kind: SignalKind
    slug: str
    side: Side
    confidence: float
    detail: str = ""


@dataclass(frozen=True)
class Fill:
    time: datetime
    slug: str
    side: Side
    size: float
    price: float
    fee_usd: float = 0.0
    paper: bool = True
