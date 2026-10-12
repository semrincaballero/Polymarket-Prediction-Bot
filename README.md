<div align="center">

# 🔮 Polymarket Prediction Bot

### Polymarket trading bot for prediction markets — CLOB order book, edge detection and arbitrage signals in your terminal.

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Textual](https://img.shields.io/badge/TUI-textual-7C3AED.svg)](https://textual.textualize.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Polymarket](https://img.shields.io/badge/Polymarket-CLOB-5B5BD6.svg)](https://polymarket.com/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](./README.md)

**Browse CLOB markets · watch the book · run probability-edge & liquidity strategies · track USDC.**

</div>

---

## 📖 Overview

**Polymarket Prediction Bot** is a **Polymarket trading bot for prediction markets** — a
keyboard-driven **terminal dashboard** for [Polymarket](https://polymarket.com/), the
**Polygon-based prediction market** with a central-limit order book (CLOB) and USDC
settlement. It bundles a markets browser, a live CLOB order-book view, a strategy engine
and a position/fill tracker into one pane — a complete **Polymarket CLOB API client
(REST + WebSocket)** in your terminal.

Polymarket shares resolve YES/NO to $1/$0 on real events: elections, crypto milestones,
sports, macro prints. Pricing a share *is* pricing a probability — the bot runs **edge
detection and liquidity provision strategies** against a fair-probability model, surfaces
**cross-market arbitrage signals (YES+NO spread, multi-outcome)**, and keeps **position
tracking and PnL history** with **risk limits and exposure controls**. A **paper trading
mode with virtual USDC balance** lets you iterate safely. **Terminal UI built with Textual
and Rich** — an **educational open-source toolkit, no financial advice**.

> ⚠️ Paper-trade by default. `--demo` simulates fills against a bundled dataset. Live order
> placement requires your own Polymarket API credentials and is gated behind explicit
> configuration.

---

## ✨ Features

| Area | What you get |
|------|--------------|
| 🔍 **Markets browser** | Filter by volume, spread, time-to-resolve, category (GAMMA). |
| 📖 **CLOB book** | YES/NO bids/asks, spread, mid, book imbalance. |
| 🧠 **Strategy engine** | Probability-edge vs. a fair-probability model, book-imbalance, liquidity. |
| 💼 **Positions** | Open YES/NO size, avg cost, uPnL in USDC, resolution countdown. |
| 🧾 **Fill log** | CLOB fills, cancels, signals — local paper trail. |
| 🎛️ **Dashboard** | Top movers, widest spreads, soonest-to-resolve, signal queue. |
| ⌨️ **Keyboard-first** | Vim bindings, `/` filter, `b` book, `s` scan, `o` order. |
| 🌑 **Theming** | Multiple palettes. |

---

## 🖥️ Screenshots

```
 ╔══════════════════════════════════════════════════════════════════════════════════════════╗
 ║ 🔮 Polymarket Bot        [1]Dash [2]Markets [3]Book [4]Strategy [5]Positions [6]Log      ║
 ╠══════════════════════════════════════════════════════════════════════════════════════════╣
 ║ Wallet: paper · 12,000 USDC   Open: 4,280 USDC   Day P&L: +312 USDC   Signals: 4         ║
 ║ ────────────────────────────────────────────────────────────────────────────────────── ║
 ║  Slug                       Market                          Price  Vol      Resolve      ║
 ║  btc-100k-by-eoy            Will BTC hit $100k by EOY       0.31   3.1M     165d         ║
 ║  fed-cut-sep                Fed cuts rates in Sep           0.68   8.4M     59d          ║
 ║  eth-4k-july                ETH above $4k in July           0.12   1.2M     12d          ║
 ║  us-recession-2026          US recession in 2026            0.42   2.7M     198d         ║
 ║                                                                                         ║
 ║  STRATEGY SIGNALS                       BOOK: btc-100k-by-eoy                              ║
 ║  ◆ fed-cut-sep    PROB-EDGE   conf .74   YES  bid .29  ask .33  spread 4.0¢             ║
 ║  ▲ eth-4k-july    IMBALANCE   conf .61   NO   bid .67  ask .71  spread 4.0¢             ║
 ║  ◆ btc-100k-eoy   PROB-EDGE   conf .69   imbalance: 61% YES                              ║
 ║                                                                                         ║
 ║  q Quit  / Filter  b Book  s Scan  o Order  t Theme  ? Help                            ║
 ╚══════════════════════════════════════════════════════════════════════════════════════════╝
```

---

## 🚀 Quick start

```bash
git clone https://github.com/semrincaballero/Polymarket-Prediction-Bot.git
cd Polymarket-Prediction-Bot
pip install -r requirements.txt

python main.py --demo     # paper-trade bundled dataset
python main.py            # live mode (needs API credentials)
```

One-click launchers (no system Python required — they unpack a bundled standalone
interpreter on first run):

```batch
run.bat        :: Windows
```
```bash
chmod +x run.sh && ./run.sh    # Linux / macOS
```

## ⚙️ Live mode credentials

```toml
# ~/.polymarket-bot/config.toml
[auth]
private_key   = "0x…"          # Polygon EOA private key (chmod 0600!)
proxy_address = "0x…"          # Polymarket proxy/signer address
api_key       = "…"
api_secret    = "…"
api_passphrase= "…"
endpoint      = "https://clob.polymarket.com"
```

Credentials are read only from the config file (mode 0600). Never commit them.

---

## ⌨️ Keybindings

| Key | Action |
|-----|--------|
| `1`–`6` | Dash · Markets · Book · Strategy · Positions · Log |
| `/` | Filter markets |
| `Enter` / `b` | Open CLOB book for the selected market |
| `s` | Run the strategy engine across the watchlist |
| `o` | Compose a paper order |
| `t` | Cycle theme |
| `q` | Quit |

---

## 🧠 Strategy engine

Built-in strategies (selectable, composable):

- **Probability-edge** — compares market price to a fair-probability model and signals when
  the edge exceeds a threshold.
- **Book-imbalance** — large YES/NO size skew as a directional cue.
- **Liquidity** — wide-spread mean-reversion toward mid.

Each signal carries a confidence `0..1` and a suggested side. The bot logs every signal; in
live mode you wire a strategy to an order template.

---

## 🗂️ Project layout

```
polymarket-prediction-bot/
├── main.py               # Entry point (unpacks bundled runtime on first launch)
├── polymarket_bot/       # Host package
│   ├── __main__.py       # `python -m polymarket_bot` entry
│   ├── cli.py            # argparse + launch
│   ├── config.py         # Config loader (TOML)
│   ├── core/             # models, strategy engine, mock data
│   └── tui/              # Textual app: screens, widgets, styles
├── support/              # Runtime support library
├── requirements.txt
├── run.bat / run.sh      # One-click launchers
└── release/              # Pre-compiled binaries (planned)
```

---

## 🔒 Security & responsible use

- **Paper-trade by default.** `--demo` never touches your wallet.
- **Keys local only**, mode 0600, never logged.
- **Risk controls**: max USDC exposure, per-market cap, daily loss limit.

---

## ❓ FAQ

<details>
<summary><b>Is Polymarket available in my region?</b></summary>

Polymarket restricts access in some jurisdictions (notably the US). This bot does not bypass
geofencing — check Polymarket's terms for your region.
</details>

<details>
<summary><b>Does it place real orders?</b></summary>

Only in live mode with your own credentials. By default it runs in paper mode and logs
signals and simulated fills. Start with `--demo`.
</details>

<details>
<summary><b>Is this affiliated with Polymarket?</b></summary>

No. Independent, unofficial community project. Polymarket is a third-party protocol.
</details>

---

## ⚠️ Disclaimer

This is an **unofficial community project**, **not affiliated with, endorsed by, or
sponsored by Polymarket**. **Not financial advice.** Trading prediction markets involves
risk of loss; no strategy in this repository is guaranteed to make money.

---

## 📄 License

MIT — see [`LICENSE`](./LICENSE).

<div align="center"><sub>Built for traders who price probabilities on-chain.</sub></div>
