"""Tab panes for the Polymarket bot dashboard."""

from polymarket_bot.tui.screens.book import BookPane
from polymarket_bot.tui.screens.dashboard import DashboardPane
from polymarket_bot.tui.screens.log_pane import LogPane
from polymarket_bot.tui.screens.markets import MarketsPane
from polymarket_bot.tui.screens.positions import PositionsPane
from polymarket_bot.tui.screens.settings import SettingsPane
from polymarket_bot.tui.screens.strategy_pane import StrategyPane

__all__ = ["BookPane", "DashboardPane", "LogPane", "MarketsPane",
           "PositionsPane", "SettingsPane", "StrategyPane"]
