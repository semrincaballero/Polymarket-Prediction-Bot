"""Strategy engine: probability-edge, book-imbalance, liquidity."""

from __future__ import annotations

from dataclasses import dataclass

from polymarket_bot.core.models import ClobBook, Market, Side, Signal, SignalKind


@dataclass(frozen=True)
class StrategyConfig:
    prob_edge_threshold_cents: float = 5.0
    imbalance_skew: float = 0.30
    liquidity_spread_cents: float = 4.0


class StrategyEngine:
    """Stateless + deterministic signal generator."""

    def __init__(self, cfg: StrategyConfig | None = None) -> None:
        self.cfg = cfg or StrategyConfig()

    def evaluate(self, market: Market, book: ClobBook,
                 *, fair_prob: float | None = None) -> list[Signal]:
        sigs: list[Signal] = []
        sigs.extend(self._prob_edge(market, fair_prob))
        sigs.extend(self._imbalance(market, book))
        sigs.extend(self._liquidity(market, book))
        return sigs

    # ------------------------------------------------------------- prob-edge

    def _prob_edge(self, m: Market, fair_prob: float | None) -> list[Signal]:
        if fair_prob is None:
            return []
        edge = m.mid - fair_prob            # +ve: market overprices YES
        thr = self.cfg.prob_edge_threshold_cents / 100.0
        if abs(edge) < thr:
            return []
        side = Side.NO if edge > 0 else Side.YES
        conf = min(1.0, abs(edge) / (thr * 2))
        return [Signal(
            kind=SignalKind.PROB_EDGE, slug=m.slug, side=side, confidence=conf,
            detail=f"mid {m.mid:.3f} vs fair {fair_prob:.3f} (edge {edge * 100:+.1f}¢)",
        )]

    # -------------------------------------------------------------- imbalance

    def _imbalance(self, m: Market, book: ClobBook) -> list[Signal]:
        imb = book.imbalance
        if abs(imb) < self.cfg.imbalance_skew:
            return []
        side = Side.YES if imb > 0 else Side.NO
        conf = min(1.0, abs(imb))
        return [Signal(
            kind=SignalKind.IMBALANCE, slug=m.slug, side=side, confidence=conf,
            detail=f"book imbalance {imb:+.2f}",
        )]

    # --------------------------------------------------------------- liquidity

    def _liquidity(self, m: Market, book: ClobBook) -> list[Signal]:
        spread_cents = m.spread * 100
        if spread_cents < self.cfg.liquidity_spread_cents:
            return []
        # Wide spread → post resting limit toward the bid/ask to capture the spread.
        side = Side.YES  # neutral choice; real impl would pick from inventory
        conf = min(1.0, spread_cents / (self.cfg.liquidity_spread_cents * 2))
        return [Signal(
            kind=SignalKind.LIQUIDITY, slug=m.slug, side=side, confidence=conf,
            detail=f"spread {spread_cents:.1f}¢ — capture via resting limit",
        )]
