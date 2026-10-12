"""Configuration loader."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
    _LOAD = tomllib.loads
else:  # pragma: no cover
    import tomli as _tomli
    _LOAD = _tomli.loads


def default_config_path() -> Path:
    from platformdirs import user_config_dir
    return Path(user_config_dir("polymarket-bot", appauthor=False)) / "config.toml"


DEFAULT_TOML = """\
[auth]
private_key    = ""
proxy_address  = ""
api_key        = ""
api_secret     = ""
api_passphrase = ""
endpoint       = "https://clob.polymarket.com"

[network]
gamma_url = "https://gamma-api.polymarket.com"
timeout_seconds = 10

[markets]
default_filter = "all"

[risk]
max_exposure_usd = 10000
per_market_cap_usd = 2000
daily_loss_limit_usd = 500

[strategies]
enabled = ["prob-edge", "imbalance", "liquidity"]

[ui]
theme = "textual-dark"
refresh_seconds = 5
"""


@dataclass(frozen=True)
class AuthConfig:
    private_key: str = ""
    proxy_address: str = ""
    api_key: str = ""
    api_secret: str = ""
    api_passphrase: str = ""
    endpoint: str = "https://clob.polymarket.com"


@dataclass(frozen=True)
class NetworkConfig:
    gamma_url: str = "https://gamma-api.polymarket.com"
    timeout_seconds: int = 10


@dataclass(frozen=True)
class MarketsConfig:
    watchlist: tuple[str, ...] = ()
    default_filter: str = "all"


@dataclass(frozen=True)
class RiskConfig:
    max_exposure_usd: float = 10000
    per_market_cap_usd: float = 2000
    daily_loss_limit_usd: float = 500


@dataclass(frozen=True)
class StrategiesConfig:
    enabled: tuple[str, ...] = ("prob-edge", "imbalance", "liquidity")


@dataclass(frozen=True)
class UIConfig:
    theme: str = "textual-dark"
    refresh_seconds: int = 5


@dataclass(frozen=True)
class Config:
    auth: AuthConfig = field(default_factory=AuthConfig)
    network: NetworkConfig = field(default_factory=NetworkConfig)
    markets: MarketsConfig = field(default_factory=MarketsConfig)
    risk: RiskConfig = field(default_factory=RiskConfig)
    strategies: StrategiesConfig = field(default_factory=StrategiesConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    demo: bool = False

    @property
    def live(self) -> bool:
        return (not self.demo) and bool(self.auth.private_key and self.auth.api_key)

    @classmethod
    def load(cls, path: Path, *, demo: bool = False) -> Config:
        path = Path(path)
        if not path.exists():
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(DEFAULT_TOML, encoding="utf-8")
            except OSError:
                pass
        raw = _LOAD(path.read_text(encoding="utf-8")) if path.exists() else {}
        return cls(
            auth=AuthConfig(**raw.get("auth", {})),
            network=NetworkConfig(**raw.get("network", {})),
            markets=MarketsConfig(watchlist=tuple(raw.get("markets", {}).get("watchlist", ())),
                                  default_filter=raw.get("markets", {}).get("default_filter", "all")),
            risk=RiskConfig(**raw.get("risk", {})),
            strategies=StrategiesConfig(enabled=tuple(raw.get("strategies", {}).get("enabled",
                                          ("prob-edge", "imbalance", "liquidity")))),
            ui=UIConfig(**raw.get("ui", {})),
            demo=demo,
        )
