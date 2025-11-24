"""
ATR Bar Detector - Identifies bars with range >= ATR threshold.
Based on TBNATRBarX.cs logic.
"""
import math
from typing import List, Optional
from src.data.data_structures import Bar, ATRBarInfo


class ATRBarDetector:
    """
    Detects ATR bars (bars with range >= ATR * multiple).
    Exact implementation from TBNATRBarX.cs
    """

    def __init__(self, period: int = 7, multiple: float = 0.75):
        """
        Initialize ATR bar detector.

        Args:
            period: ATR calculation period (default 7)
            multiple: ATR multiple for threshold (default 0.75)
        """
        self.period = period
        self.multiple = multiple
        self.bars: List[Bar] = []
        self.atr_values: List[float] = []
        self.atr_bar_history: List[Optional[ATRBarInfo]] = []

    def calculate_true_range(self, current_bar: Bar, previous_bar: Optional[Bar]) -> float:
        """
        Calculate true range for a bar.

        TR = max(high - low, |high - prev_close|, |low - prev_close|)
        """
        if previous_bar is None:
            return current_bar.high - current_bar.low

        return max(
            current_bar.high - current_bar.low,
            abs(current_bar.high - previous_bar.close),
            abs(current_bar.low - previous_bar.close)
        )

    def calculate_atr(self, bars: List[Bar]) -> float:
        """
        Calculate ATR for given bars.
        Uses simple moving average of true ranges.

        Args:
            bars: List of bars (must be at least self.period + 1 length)

        Returns:
            ATR value
        """
        if len(bars) < self.period + 1:
            return 0.0

        # Calculate true ranges for the last 'period' bars
        true_ranges = []
        for i in range(len(bars) - self.period, len(bars)):
            prev_bar = bars[i - 1] if i > 0 else None
            tr = self.calculate_true_range(bars[i], prev_bar)
            true_ranges.append(tr)

        # Average true range
        atr = sum(true_ranges) / len(true_ranges)

        # From TBNATRBarX.cs line 60: Math.Ceiling(ATR(7)[0]/.01) * .01
        # This rounds ATR up to nearest 0.01
        atr = math.ceil(atr / 0.01) * 0.01

        return atr

    def is_atr_bar(self, bar: Bar, atr: float) -> Optional[str]:
        """
        Check if bar qualifies as ATR bar.

        From TBNATRBarX.cs lines 61-95:
        - highlowRange = Math.Ceiling(Math.Abs(Open[0] - Close[0]) / .01) * .01
        - threshold = atr * multiple
        - Bullish: Close > Open AND highlowRange >= threshold
        - Bearish: Close < Open AND highlowRange >= threshold

        Args:
            bar: Bar to check
            atr: Current ATR value

        Returns:
            'BULLISH', 'BEARISH', or None
        """
        if atr == 0:
            return None

        # From TBNATRBarX.cs line 61
        bar_range = abs(bar.open - bar.close)
        bar_range = math.ceil(bar_range / 0.01) * 0.01

        # From TBNATRBarX.cs line 62
        threshold = math.ceil((self.multiple * atr) / 0.01) * 0.01

        # From TBNATRBarX.cs lines 77-95
        if bar.close > bar.open and bar_range >= threshold:
            return 'BULLISH'
        elif bar.close < bar.open and bar_range >= threshold:
            return 'BEARISH'

        return None

    def on_bar(self, bar: Bar) -> Optional[str]:
        """
        Process a new bar and detect if it's an ATR bar.

        Args:
            bar: New bar to process

        Returns:
            'BULLISH', 'BEARISH', or None
        """
        self.bars.append(bar)

        # Need at least period + 1 bars to calculate ATR
        if len(self.bars) < self.period + 1:
            self.atr_values.append(0.0)
            self.atr_bar_history.append(None)
            return None

        # Calculate current ATR
        atr = self.calculate_atr(self.bars)
        self.atr_values.append(atr)

        # Check if current bar is ATR bar
        atr_bar_type = self.is_atr_bar(bar, atr)

        # Store ATR bar info for later target calculation
        if atr_bar_type:
            atr_bar_info = ATRBarInfo(
                bar_index=len(self.bars) - 1,
                bar_type=atr_bar_type,
                open_price=bar.open,
                close_price=bar.close,
                timestamp=bar.timestamp
            )
            self.atr_bar_history.append(atr_bar_info)
        else:
            self.atr_bar_history.append(None)

        return atr_bar_type

    def get_current_atr(self) -> float:
        """Get the most recent ATR value."""
        if not self.atr_values:
            return 0.0
        return self.atr_values[-1]

    def find_opposite_atr_bar(self, current_index: int, direction: str,
                              lookback: int = 20) -> Optional[ATRBarInfo]:
        """
        Find the most recent opposite direction ATR bar.

        Args:
            current_index: Current bar index
            direction: 'LONG' or 'SHORT' (looking for opposite)
            lookback: Maximum bars to look back

        Returns:
            ATRBarInfo if found, None otherwise
        """
        if direction == 'LONG':
            target_type = 'BEARISH'  # Long trade looks for prior bearish ATR bar
        else:
            target_type = 'BULLISH'  # Short trade looks for prior bullish ATR bar

        # Search backwards from current_index - 1
        for i in range(current_index - 1, max(-1, current_index - lookback - 1), -1):
            if i < 0 or i >= len(self.atr_bar_history):
                continue

            atr_bar_info = self.atr_bar_history[i]
            if atr_bar_info and atr_bar_info.bar_type == target_type:
                return atr_bar_info

        return None

    def get_atr_at_index(self, index: int) -> float:
        """Get ATR value at specific index."""
        if index < 0 or index >= len(self.atr_values):
            return 0.0
        return self.atr_values[index]
