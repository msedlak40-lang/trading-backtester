"""
Core data structures for the backtesting system.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class Bar:
    """Represents a single OHLCV bar."""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

    # Computed properties
    @property
    def is_bullish(self) -> bool:
        """Bar closed above open."""
        return self.close > self.open

    @property
    def is_bearish(self) -> bool:
        """Bar closed below open."""
        return self.close < self.open

    @property
    def bar_range(self) -> float:
        """Open to close range (unsigned)."""
        return abs(self.close - self.open)

    @property
    def true_range(self) -> float:
        """High to low range."""
        return self.high - self.low


@dataclass
class Zone21State:
    """
    Complete state tracking for Zone21B indicator.
    Mirrors the state variables in Zone21B2.cs
    """
    # Buy side (downward pattern) state
    down_bar_one: bool = False
    down_bar_one_low: float = 0.0
    down_bar_one_high: float = 0.0

    down_bar_two: bool = False
    down_bar_two_low: float = 0.0
    down_bar_two_high: float = 0.0

    swing_high: float = 0.0
    swing_high_bars: int = 0
    take_swing_high: bool = False
    take_bar_high: bool = False

    down_within_bar: bool = False
    down_within_high: float = 0.0
    down_within_low: float = 0.0

    down_4th_bar: bool = False
    down_4th_bar_high: float = 0.0
    down_4th_bar_low: float = 0.0

    under_bar: bool = False
    under_bar_high: float = 0.0
    under_bar_low: float = 0.0

    i_bar_1_down: bool = False
    i_bar_1_down_low: float = 0.0
    i_bar_1_down_high: float = 0.0

    i_bar_2_down: bool = False
    i_bar_2_down_low: float = 0.0
    i_bar_2_down_high: float = 0.0

    i_bar_3_down: bool = False
    i_bar_3_down_low: float = 0.0
    i_bar_3_down_high: float = 0.0

    stored_4th_low: float = 0.0
    lower_low: bool = False

    # Zeta bar (buy setup completion)
    zeta_bar: bool = False
    zeta_bar_high: float = 0.0
    zeta_bar_low: float = 0.0
    zeta_bar_close: float = 0.0
    closes_above_z: int = 1
    zeta_bar_ft: bool = False
    possible_low: float = float('inf')

    # Buy zone
    old_running_low: float = float('inf')
    running_low: float = float('inf')
    stored_swing_high: float = 0.0
    buy_zone: bool = False
    buy_zone_high: float = 0.0
    buy_zone_low: float = 0.0
    buy_zone_count: int = 0

    # Sell side (upward pattern) state - mirror of buy side
    up_bar_one: bool = False
    up_bar_one_low: float = 0.0
    up_bar_one_high: float = 0.0

    up_bar_two: bool = False
    up_bar_two_low: float = 0.0
    up_bar_two_high: float = 0.0

    swing_low: float = float('inf')
    swing_low_bars: int = 0
    take_swing_low: bool = False
    take_bar_low: bool = False

    up_within_bar: bool = False
    up_within_high: float = 0.0
    up_within_low: float = 0.0

    up_4th_bar: bool = False
    up_4th_bar_high: float = 0.0
    up_4th_bar_low: float = 0.0

    over_bar: bool = False
    over_bar_high: float = 0.0
    over_bar_low: float = 0.0

    i_bar_1_up: bool = False
    i_bar_1_up_low: float = 0.0
    i_bar_1_up_high: float = 0.0

    i_bar_2_up: bool = False
    i_bar_2_up_low: float = 0.0
    i_bar_2_up_high: float = 0.0

    i_bar_3_up: bool = False
    i_bar_3_up_low: float = 0.0
    i_bar_3_up_high: float = 0.0

    stored_4th_high: float = 0.0
    higher_high: bool = False

    # Alpha bar (sell setup completion)
    alpha_bar: bool = False
    alpha_bar_high: float = 0.0
    alpha_bar_low: float = 0.0
    alpha_bar_close: float = 0.0
    closes_below_a: int = 1
    alpha_bar_ft: bool = False
    possible_high: float = 0.0

    # Sell zone
    old_running_high: float = 0.0
    running_high: float = 0.0
    stored_swing_low: float = 0.0
    sell_zone: bool = False
    sell_zone_high: float = 0.0
    sell_zone_low: float = 0.0
    sell_zone_count: int = 0


@dataclass
class Trade:
    """Represents a single trade with entry and exit details."""
    entry_bar: int
    entry_time: datetime
    entry_price: float
    direction: str  # 'LONG' or 'SHORT'
    position_size: int
    stop_price: float
    target_price: float
    atr_at_entry: float

    exit_bar: Optional[int] = None
    exit_time: Optional[datetime] = None
    exit_price: Optional[float] = None
    exit_reason: Optional[str] = None  # 'STOP', 'TARGET'
    pnl: Optional[float] = None
    pnl_percent: Optional[float] = None
    bars_in_trade: Optional[int] = None

    def close_trade(self, bar_index: int, bar_time: datetime, exit_price: float,
                    reason: str, tick_size: float, tick_value: float) -> None:
        """Close the trade and calculate P&L."""
        self.exit_bar = bar_index
        self.exit_time = bar_time
        self.exit_price = exit_price
        self.exit_reason = reason
        self.bars_in_trade = bar_index - self.entry_bar

        # Calculate P&L
        if self.direction == 'LONG':
            pnl_points = (exit_price - self.entry_price) * self.position_size
        else:  # SHORT
            pnl_points = (self.entry_price - exit_price) * self.position_size

        pnl_ticks = pnl_points / tick_size
        self.pnl = pnl_ticks * tick_value


@dataclass
class Position:
    """Represents an active position."""
    trade: Trade
    is_active: bool = True

    def close(self, bar_index: int, bar_time: datetime, exit_price: float,
              reason: str, tick_size: float, tick_value: float) -> None:
        """Close the position."""
        self.trade.close_trade(bar_index, bar_time, exit_price, reason, tick_size, tick_value)
        self.is_active = False


@dataclass
class DivergenceState:
    """Tracks divergence detection state."""
    active: bool = False
    type: Optional[str] = None  # 'BULLISH' or 'BEARISH'
    nq_swing_value: float = 0.0
    composite_swing_value: float = 0.0
    bars_since_new_swing: int = 0
    new_swing_detected: bool = False


@dataclass
class ATRBarInfo:
    """Information about ATR bars for target calculation."""
    bar_index: int
    bar_type: str  # 'BULLISH' or 'BEARISH'
    open_price: float
    close_price: float
    timestamp: datetime
