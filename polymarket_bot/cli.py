"""CLI entry point."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from polymarket_bot import __version__
from polymarket_bot.config import Config, default_config_path


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="polymarket-bot",
                                description="Terminal prediction-market bot for Polymarket.")
    p.add_argument("--version", "-V", action="version", version=f"polymarket-bot {__version__}")
    p.add_argument("--config", type=Path, default=None)
    p.add_argument("--demo", action="store_true", help="paper-trade a bundled dataset")
    p.add_argument("--market", type=str, default=None, help="open directly on a market slug")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    demo = args.demo or os.environ.get("POLYMARKET_BOT_DEMO", "") == "1"
    config = Config.load(args.config or Path(os.environ.get("POLYMARKET_BOT_CONFIG",
                                                            str(default_config_path()))), demo=demo)

    try:
        from polymarket_bot.tui.app import PolymarketBotApp
    except ImportError as exc:  # pragma: no cover
        print(f"error: TUI deps missing ({exc}). Run `pip install -e .`.", flush=True)
        return 2

    PolymarketBotApp(config=config, initial_market=args.market).run()
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
